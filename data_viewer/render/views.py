from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
	if request.user.is_authenticated():
		#TODO: authorization status
		return render_to_response('dashboard.html', {}, context_instance=RequestContext(request))
	return render_to_response('home.html', {}, context_instance=RequestContext(request))

def test(request):
	return HttpResponse(request.user.username)
