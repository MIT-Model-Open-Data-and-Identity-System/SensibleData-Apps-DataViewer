import json
from django.contrib.auth.models import User
from django.core.cache import get_cache
from django.http import HttpResponse
from djcelery.models import TaskMeta
from django_sensible.identity import getAttributes
from django_sensible.tasks import fetch_data_worker, notify_user


def export(request):
	start_url = request.REQUEST['query_url']
	if "pretty" in start_url:
		return HttpResponse("This format is not supported for data export. Please choose JSON or CSV.", status=500, content_type="text/plain")

	username = request.user.username

	user_email = json.loads(getAttributes(User.objects.get(username=username), ['email'])).get("email")
	if not user_email:
		return HttpResponse("DataViewer does not have permission to use your email. Grant permission using the My Profile button.", status=500, content_type="text/plain")

	cache = get_cache('default')
	if cache.get(username):
		if TaskMeta.objects.get_task(cache.get(username)).status == "PENDING":
			return HttpResponse("You have already started an export request. Please wait for it to be over before starting a new one.", status=500, content_type="text/plain")

	cache.set(username, fetch_data_worker.apply_async((start_url, username), link=notify_user.s(username)))

	return HttpResponse("Your data export has started. You will receive an e-mail at " + user_email + " when your file is ready.")
