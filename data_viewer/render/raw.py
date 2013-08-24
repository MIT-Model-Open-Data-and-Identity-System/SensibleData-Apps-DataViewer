from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django_sensible import oauth2

@login_required
def location(request):
	#TODO move this to a library
	#TODO tokens that are not expired
	tokens = {}
	t1 = oauth2.getToken(request.user, 'connector_raw.all_data')
	if not t1 == None: tokens['connector_raw.all_data'] = t1
	t2 = oauth2.getToken(request.user, 'connector_raw.all_data_researcher')
	if not t2 == None: tokens['connector_raw.all_data_researcher'] = t2


	return render_to_response('location.html', {'tokens': tokens}, context_instance=RequestContext(request))

