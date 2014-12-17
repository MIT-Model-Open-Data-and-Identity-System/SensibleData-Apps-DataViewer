
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

def build_response_phone_data(request, endpoint):
	tokens = getTokens(request)
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/' + endpoint
	users_to_return =  request.GET.get("users_to_return", "")
	start_date = request.GET.get("start_date", "")
	end_date = request.GET.get("end_date", "")

	scope = 'connector_raw.all_data=checked'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_' + endpoint + '.json').read()), "fields")
	if not tokens:
		return get_start_auth_response(request, scope)

	return render_to_response('todo_data2_trans.html', {'tokens': tokens,
														'example_doc': example_doc,
														'base_url': base_url,
														'users_to_return': users_to_return,
														'start_date': start_date,
														'end_date': end_date, endpoint: True}, context_instance=RequestContext(request))

def build_response_facebook(request, endpoint):
	tokens = getTokens(request)
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/facebook/' + endpoint

	scope = 'connector_raw.all_data=checked'
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_facebook.json').read()), "fields")
	if not tokens:
		return get_start_auth_response(request, scope)

	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc, 'base_url': base_url, endpoint:True}, context_instance=RequestContext(request))

def build_response_questionnaire(request, endpoint):
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/' + endpoint
	example_doc = create_links(json.loads(open(settings.ROOT_DIR+'render/example_questionnaire.json').read()), "fields")
	example_doc1 = create_links(json.loads(open(settings.ROOT_DIR+'render/example_questionnaire2.json').read()),"questions")

	if not tokens:
		return get_start_auth_response(request, scope)

	form_versions = json.dumps(settings.QUESTIONNAIRE_VERSIONS)
	form_versions_labels = settings.QUESTIONNAIRE_VERSIONS.keys()
	return render_to_response('todo_data2_trans.html', {'tokens': tokens, 'example_doc': example_doc, 'example_doc1': example_doc1, 'base_url': base_url, 'questionnaire':True, 'form_versions': form_versions, 'form_version_labels': form_versions_labels}, context_instance=RequestContext(request))

def get_start_auth_response(request, scope):
	return render_to_response('sensible/start_auth.html',
							  {'scope': scope, 'dashboard_url': settings.SERVICE_URL + 'researcher/'},
							  context_instance=RequestContext(request))

@login_required
def location(request):
	return build_response_phone_data(request, "location")

@login_required
def bluetooth(request):
	return build_response_phone_data(request, "bluetooth")

@login_required
def calllog(request):
	return build_response_phone_data(request, "calllog")

@login_required
def sms(request):
	return build_response_phone_data(request, "sms")

@login_required
def wifi(request):
	return build_response_phone_data(request, "wifi")

@login_required
def likes(request):
	return build_response_facebook(request, "likes")

@login_required
def friends(request):
	return build_response_facebook(request, "friends")

@login_required
def birthday(request):
	return build_response_facebook(request, "birthday")

@login_required
def education(request):
	return build_response_facebook(request, "education")

@login_required
def friendlists(request):
	return build_response_facebook(request, "friendlists")

@login_required
def groups(request):
	return build_response_facebook(request, "groups")

@login_required
def hometown(request):
	return build_response_facebook(request, "hometown")

@login_required
def interests(request):
	return build_response_facebook(request, "interests")

@login_required
def locationfacebook(request):
	return build_response_facebook(request, "location")

@login_required
def political(request):
	return build_response_facebook(request, "political")

@login_required
def religion(request):
	return build_response_facebook(request, "religion")

@login_required
def work(request):
	return build_response_facebook(request, "work")

def grades(request):
	return build_response_phone_data(request, "grades")

@login_required
def questionnaire(request):
	return build_response_questionnaire(request, "connector_raw/v1/questionnaire")

@login_required
def questionnaire_grouped_by_user(request):
	return build_response_questionnaire(request, "connector_answer/v1/aggregate_questionnaire_question/get_aggregated_questionnaire_data")

@login_required
def users(request):
	
	tokens = getTokens(request)
	scope = 'connector_raw.all_data=checked'
	base_url = settings.SERVICE_URL+'connectors/connector_raw/v1/'

	if not tokens:
		return get_start_auth_response(request, scope)

	return render_to_response('users.html', {'tokens': tokens, 'base_url': base_url}, context_instance=RequestContext(request))


def create_links(document, field_name):
	link_dictionary = {}
	for key in document:
		link_dictionary["<a href='#' onclick=\"$('#" + field_name + "')[0].value += '" + key + ",'\">" + str(key) + "</a>"] = document[key]
	return json.dumps(link_dictionary, sort_keys=True, indent=2, separators=(',', ':')).replace('\\"', '"')