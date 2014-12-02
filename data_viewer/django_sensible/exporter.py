import json
import os
import smtplib
from urllib import urlencode
import urllib2
import urlparse
from celery.task import task
import time
from django.conf import settings
from django.contrib.auth.models import User
from ntlm.smtp import ntlm_authenticate
from django_sensible import SECURE_CONFIG
from django_sensible.identity import getAttributes
from email.mime.text import MIMEText as text

RETRY_PERIOD_SECONDS = 300

def get_format(url):
	parsed = urlparse.urlparse(url)
	return urlparse.parse_qs(parsed.query)['format'][0]


def get_temp_url(url, results_format="json"):
	scheme, netloc, path, query_string, fragment = urlparse.urlsplit(url)
	params = urlparse.parse_qs(query_string)
	params['format'] = results_format
	temp_query_string = urlencode(params, doseq=True)
	return urlparse.urlunsplit((scheme, netloc, path, temp_query_string, fragment))


def get_exporter(results_format, results_filename):
	if results_format == 'csv':
		return CSVExporter(results_filename)
	elif results_format == 'json':
		return JSONExporter(results_filename)


@task
def fetch_data_worker(start_url, user):
	results_filename = settings.EXPORTED_DATA_FOLDER + user + "_" + str(int(time.time())) + settings.EXPORT_FILE_SUFFIX
	results_format = get_format(start_url)
	export_tool = get_exporter(results_format, results_filename)
	message = ""
	retry_start_time = None
	while True:
		temp_url = get_temp_url(start_url)
		try:
			response = json.loads(urllib2.urlopen(temp_url).read())
		except urllib2.HTTPError, e:
			if not retry_start_time:
				retry_start_time = time.time()

			if time.time() - retry_start_time < RETRY_PERIOD_SECONDS:
				continue

			error_message = e.read()
			if "meta" in error_message:
				message = json.loads(error_message)["meta"]["status"]["desc"]
			else:
				message = error_message
			break

		#reset retry timer on success
		if retry_start_time:
			retry_start_time = None

		results = response.get('results')

		if not results:
			break

		for result in results:
			export_tool.write_line(result)

		if "paging" not in response["meta"]:
			break

		start_url = response["meta"]["paging"]["links"]["next"]
	export_tool.close_file()
	return {"file_url": settings.DATA_EXPORT_URL + os.path.basename(results_filename), "message": message}

@task
def notify_user(result, username, user_email):
	if not user_email:
		return
	first_name = json.loads(getAttributes(User.objects.get(username=username), ['first_name'])).get("first_name")
	if not first_name:
		first_name = "user"
	notification_message = "Dear " + first_name + ",\n\nYour data export is complete. You can download the file from the link below. Please note that after 1 hour, the file will be deleted."
	notification_message += "\n\nDownload link: " + result["file_url"]
	if result["message"]:
		notification_message += "\n\nPlease note: " + result["message"]
	notification_message += "\n\nKind regards,\nThe SensibleDTU team"
	send_email(user_email, notification_message)


def send_email(receiver_email, message):
	username = SECURE_CONFIG.SUPPORT_EMAIL_USERNAME
	password = SECURE_CONFIG.SUPPORT_EMAIL_PASSWORD

	server = smtplib.SMTP('mail.dtu.dk:587')
	server.starttls()

	ntlm_authenticate(server, username, password)

	fromaddr = SECURE_CONFIG.SUPPORT_EMAIL_ADDRESS
	toaddrs = receiver_email

	m = text(message)

	m['Subject'] = 'Data export request'
	m['From'] = fromaddr
	m['To'] = toaddrs

	print server.sendmail(fromaddr, toaddrs, m.as_string())
	server.quit()

class Exporter(object):

	def __init__(self, output_file_name):
		self.output_file = open(output_file_name, "a")

	def close_file(self):
		self.output_file.close()

	def write_line(self, line):
		pass


class CSVExporter(Exporter):

	def __init__(self, output_file_name):
		self.column_names = []
		super(CSVExporter, self).__init__(output_file_name)

	def write_line(self, line):
		if not self.column_names:
			self.column_names = line.keys()
			self.output_file.write(",".join(self.column_names) + "\n")
		self.output_file.write(",".join([str(line[column_name]) for column_name in self.column_names]) + "\n")


class JSONExporter(Exporter):

	def write_line(self, line):
		self.output_file.write(json.dumps(line) + "\n")
