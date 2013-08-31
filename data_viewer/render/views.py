from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

def home(request):
	if request.user.is_authenticated():
		return render_to_response('dashboard.html', {}, context_instance=RequestContext(request))
		#scope = 'connector_raw.all_data=checked'
		#return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))
	return render_to_response('home.html', {}, context_instance=RequestContext(request))

def test(request):
	return HttpResponse(request.user.username)
