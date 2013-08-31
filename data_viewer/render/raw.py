from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django_sensible import oauth2
import json
from django_sensible import SECURE_CONFIG
from django.conf import settings
from django.core.urlresolvers import reverse
import utils


def getTokens(request):
	#TODO change URLs
	tokens = {}
	t1 = oauth2.getToken(request.user, 'connector_raw.all_data')
	#try to refresh token
	r = oauth2.query(settings.SERVICE_URL+'connectors/connector_raw/v1/location/', t1, '&dummy=True&decrypted=True', SECURE_CONFIG.CLIENT_ID, SECURE_CONFIG.CLIENT_SECRET, settings.APPLICATION_URL[-1]+reverse('grant'), settings.SERVICE_REFRESH_TOKEN_URL)
	
	t1 = oauth2.getToken(request.user, 'connector_raw.all_data')
	if not t1 == None: tokens['connector_raw_all_data'] = t1
	
	t2 = oauth2.getToken(request.user, 'connector_raw.all_data_researcher')
	r = oauth2.query(settings.SERVICE_URL+'connectors/connector_raw/v1/location/', t2, '&dummy=True&decrypted=False', SECURE_CONFIG.CLIENT_ID, SECURE_CONFIG.CLIENT_SECRET, settings.APPLICATION_URL[-1]+reverse('grant'), settings.SERVICE_REFRESH_TOKEN_URL)
	
	t2 = oauth2.getToken(request.user, 'connector_raw.all_data_researcher')
	if not t2 == None: tokens['connector_raw_all_data_researcher'] = t2
	return tokens

@login_required
def location(request):
	
	tokens = getTokens(request)
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/location/'

	scope = 'connector_raw.all_data=checked'

	example_doc = utils.createExampleDoc(json.loads(open(settings.ROOT_DIR+'render/example_location.json').read()))

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('location.html', {'tokens': tokens, 'example_doc': example_doc, 'base_url': base_url}, context_instance=RequestContext(request))

@login_required
def users(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('users.html', {'tokens': tokens}, context_instance=RequestContext(request))

