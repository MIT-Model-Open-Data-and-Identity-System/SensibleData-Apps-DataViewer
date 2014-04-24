import hashlib
import json
from django.conf import settings
import os
import smtplib
import urllib2
from celery.task import task
import time
from django.contrib.auth.models import User
from ntlm.smtp import ntlm_authenticate
from django_sensible import SECURE_CONFIG
from django_sensible.identity import getAttributes
from email.mime.text import MIMEText as text

EXPORTED_DATA_FOLDER = "/Users/radugatej/DTU/sensibleDTU/data/exported_data/"

@task
def fetch_data_worker(start_url, user):

	service_response = json.loads(urllib2.urlopen(start_url).read())
	print service_response
	results = service_response.get("results")
	results_file = open(EXPORTED_DATA_FOLDER + user + "_" + hashlib.sha256("".join(service_response.keys())).hexdigest() + "_" + str(int(time.time())), "a")
	print results
	while results:
		for result in results:
			results_file.write(str(result) + "\n")
		results_file.flush()
		try:
			next_request = service_response["meta"]["paging"]["links"]["next"]
			service_response = json.loads(urllib2.urlopen(next_request).read())
			results = service_response.get("results")
		except KeyError:
			break
	results_file.close()

	return settings.DATA_EXPORT_URL + os.path.basename(results_file.name)

@task
def notify_user(result, username):

	email = json.loads(getAttributes(User.objects.get(username=username), ['email'])).get("email")
	if not email:
		return
	first_name = json.loads(getAttributes(User.objects.get(username=username), ['first_name'])).get("first_name")
	if not first_name:
		first_name = "user"
	notification_message = "Dear " + first_name + ",\n\nYour data export is complete. You can download the file from the link below. Please note that after 1 hour, the file will be deleted."
	notification_message += "\n\nDownload link: " + result
	notification_message += "\n\nKind regards,\nThe SensibleDTU team"
	send_email(email, notification_message)

def send_email(receiver_email, message):
	username = SECURE_CONFIG.SUPPORT_EMAIL_USERNAME
	password = SECURE_CONFIG.SUPPORT_EMAIL_PASSWORD

	server = smtplib.SMTP('mail.dtu.dk:587')
	server.starttls()

	ntlm_authenticate(server, username, password)

	fromaddr = SECURE_CONFIG.SUPPORT_EMAIL_ADDRESS
	toaddrs  = receiver_email

	m = text(message)

	m['Subject'] = 'Data export request'
	m['From'] = fromaddr
	m['To'] = toaddrs

	print server.sendmail(fromaddr, toaddrs, m.as_string())
	server.quit()

