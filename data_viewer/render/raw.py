
import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django_sensible import oauth2
from django_sensible import SECURE_CONFIG


def getTokens(request):
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
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/location'
	
	scope = 'connector_raw.all_data=checked'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_location.json').read()), "fields")
	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc, 'base_url': base_url, 'location':True}, context_instance=RequestContext(request))

@login_required
def bluetooth(request):
	
	tokens = getTokens(request)
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/bluetooth'

	scope = 'connector_raw.all_data=checked'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_bluetooth.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc, 'base_url': base_url,  'bluetooth':True}, context_instance=RequestContext(request))

@login_required
def calllog(request):
	
	tokens = getTokens(request)
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/calllog'

	scope = 'connector_raw.all_data=checked'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_calllog.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc, 'base_url': base_url, 'calllog': True}, context_instance=RequestContext(request))

@login_required
def sms(request):
	
	tokens = getTokens(request)
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/sms'

	scope = 'connector_raw.all_data=checked'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_sms.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc, 'base_url': base_url,'sms': True}, context_instance=RequestContext(request))

@login_required
def wifi(request):
	
	tokens = getTokens(request)
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/wifi'

	scope = 'connector_raw.all_data=checked'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_wifi.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc, 'base_url': base_url,'wifi':True}, context_instance=RequestContext(request))

@login_required
def likes(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/likes/'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'likes':True}, context_instance=RequestContext(request))

@login_required
def friends(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/friends'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'friends':True}, context_instance=RequestContext(request))

@login_required
def birthday(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/birthday'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'birthday':True}, context_instance=RequestContext(request))

@login_required
def education(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/education'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'education':True}, context_instance=RequestContext(request))

@login_required
def friendlists(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/friendlists'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'friendlists':True}, context_instance=RequestContext(request))

@login_required
def groups(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/groups'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'groups':True}, context_instance=RequestContext(request))

@login_required
def hometown(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/hometown'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'hometown':True}, context_instance=RequestContext(request))

@login_required
def interests(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/interests'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'interests':True}, context_instance=RequestContext(request))

@login_required
def locationfacebook(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/location'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'locationfacebook':True}, context_instance=RequestContext(request))

@login_required
def political(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/political'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'political':True}, context_instance=RequestContext(request))

@login_required
def religion(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/religion'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'religion':True}, context_instance=RequestContext(request))

@login_required
def work(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/work'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('todo_data2.html', {'tokens': tokens, 'example_doc': example_doc,'base_url': base_url, 'work':True}, context_instance=RequestContext(request))

@login_required
def questionnaire(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/questionnaire'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_questionnaire.json').read()), "fields")
	example_doc1 = create_links(json.loads(open(settings.ROOT_DIR+'render/example_questionnaire2.json').read()),"questions")

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	form_versions = json.dumps(settings.QUESTIONNAIRE_VERSIONS)
	form_versions_labels = settings.QUESTIONNAIRE_VERSIONS.keys()
	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc, 'example_doc1': example_doc1, 'base_url': base_url, 'questionnaire':True, 'form_versions': form_versions, 'form_version_labels': form_versions_labels}, context_instance=RequestContext(request))

@login_required
def users(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/'

	if not tokens:
		return render_to_response('sensible/start_auth.html', {'scope': scope, 'dashboard_url': settings.SERVICE_URL+'researcher/'}, context_instance=RequestContext(request))

	return render_to_response('users.html', {'tokens': tokens, 'base_url': base_url}, context_instance=RequestContext(request))


def create_links(document, field_name):
	link_dictionary = {}
	for key in document:
		link_dictionary["<a href='#' onclick=\"$('#" + field_name + "')[0].value += '" + key + ",'\">" + str(key) + "</a>"] = document[key]
	return json.dumps(link_dictionary, sort_keys=True, indent=2, separators=(',', ':')).replace('\\"', '"')