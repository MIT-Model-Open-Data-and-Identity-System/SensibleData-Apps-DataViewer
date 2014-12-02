import calendar
from collections import OrderedDict
import json
import urllib
import urllib2
import datetime
from dateutil import rrule
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from render.raw import getTokens, get_start_auth_response

def get_month_day_range(date):
	"""
	For a date 'date' returns the start and end date for the month of 'date'.

	Month with 31 days:
	>>> date = datetime.date(2011, 7, 27)
	>>> get_month_day_range(date)
	(datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))

	Month with 28 days:
	>>> date = datetime.date(2011, 2, 15)
	>>> get_month_day_range(date)
	(datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
	"""
	first_day = date.replace(day = 1)
	last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
	return first_day, last_day

@login_required
def get_quality_users_for_period(request):
	start = request.GET.get("start")
	end = request.GET.get("end")

	start = datetime.datetime.strptime(start, "%Y-%m-%d")
	end = datetime.datetime.strptime(end, "%Y-%m-%d")
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	if not tokens:
		return get_start_auth_response(request, scope)

	monthly_quality = []
	for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
		data_quality_url = settings.SERVICE_URL + 'connectors/connector_answer/v1/data_quality_question/get_data_stats_for_period/?'
		month_day_range = get_month_day_range(dt)
		params = urllib.urlencode({"start_date": month_day_range[0].strftime("%Y-%m-%d"), "end_date": month_day_range[1].strftime("%Y-%m-%d"), "data_type": request.GET.get("data_type"), "bearer_token": tokens.get("connector_raw.all_data_researcher")})
		quality = json.loads(urllib2.urlopen(data_quality_url + params).read())
		good_users = [doc["user"] for doc in quality if doc["quality"] > 0.7]

		monthly_quality.append({"month": dt.strftime("%Y %b"),
								"month_start": month_day_range[0].strftime("%Y-%m-%d"),
								"month_end": month_day_range[1].strftime("%Y-%m-%d"),
								"quality": len(good_users),
								"good_users": good_users})
	return HttpResponse(json.dumps(monthly_quality), status=200, content_type="application/json")

@login_required
def data_quality(request):

	quality_types = OrderedDict({"bluetooth": "Bluetooth", "location": "Location", "calllog": "Call Log", "sms": "SMS"})
	return render_to_response("data_quality.html", {"quality_types": quality_types, "root_url": settings.BASE_URL + settings.ROOT_URL}, context_instance=RequestContext(request))
