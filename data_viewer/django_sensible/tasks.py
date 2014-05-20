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

	service_response = parse_response(urllib2.urlopen(start_url).read())
	results = service_response.get("results")
	results_file = open(EXPORTED_DATA_FOLDER + user + "_" + str(int(time.time())), "a")
	message = ""
	while results:
		for result in results:
			results_file.write(str(result) + "\n")
		results_file.flush()
		try:
			next_request = service_response.get("next")
			if next_request:
				service_response = parse_response(urllib2.urlopen(next_request).read())
			results = service_response.get("results")
		except BaseException, e:
			if "expired" in service_response:
				message = "Your token has expired during export, therefore the results are incomplete."
	results_file.close()

	return {"file_url": settings.DATA_EXPORT_URL + os.path.basename(results_file.name), "message": message}

def parse_response(response):
	parsed_response = {}
	if str(response).startswith("#"):#means we have CSV
		meta = "".join([line.split("#")[1] for line in str(response).split("\n") if line.startswith("#")])
		meta = json.loads(meta)
		if meta.get("paging"):
			parsed_response["next"] = meta["paging"]["links"]["next"]
		parsed_response["results"] = [line for line in str(response).split("\n") if not line.startswith("#")][1:]
	else:
		json_response = json.loads(response)
		if json_response["meta"].get("paging"):
			parsed_response["next"] = json_response["meta"]["paging"]["links"]["next"]
		parsed_response["results"] = json_response["results"]

	return parsed_response

@task
def notify_user(result, username):

	email = json.loads(getAttributes(User.objects.get(username=username), ['email'])).get("email")
	if not email:
		return
	first_name = json.loads(getAttributes(User.objects.get(username=username), ['first_name'])).get("first_name")
	if not first_name:
		first_name = "user"
	notification_message = "Dear " + first_name + ",\n\nYour data export is complete. You can download the file from the link below. Please note that after 1 hour, the file will be deleted."
	notification_message += "\n\nDownload link: " + result["file_url"]
	if result["mesage"]: notification_message += "\n\nPlease note: " + result["message"]
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

