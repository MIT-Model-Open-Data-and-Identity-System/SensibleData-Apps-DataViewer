from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^i18n/', include('django.conf.urls.i18n')),
	url(r'test', 'render.views.test', name='test'),
	url(r'raw_phone_location', 'render.raw.location', name='raw_phone_location'),
	url(r'raw_phone_bluetooth', 'render.raw.bluetooth', name='raw_phone_bluetooth'),
	url(r'raw_phone_calllog', 'render.raw.calllog', name='raw_phone_calllog'),
	url(r'raw_phone_sms', 'render.raw.sms', name='raw_phone_sms'),
	url(r'raw_phone_wifi', 'render.raw.wifi', name='raw_phone_wifi'),
	url(r'raw_facebook_birthday', 'render.raw.birthday', name='raw_facebook_birthday'),
	url(r'raw_facebook_education', 'render.raw.education', name='raw_facebook_education'),
	url(r'raw_facebook_likes', 'render.raw.likes', name='raw_facebook_likes'),
	url(r'raw_facebook_friends', 'render.raw.friends', name='raw_facebook_friends'),
	url(r'raw_facebook_friendlists', 'render.raw.friendlists', name='raw_facebook_friendlists'),
	url(r'raw_facebook_groups', 'render.raw.groups', name='raw_facebook_groups'),
	url(r'raw_facebook_hometown', 'render.raw.hometown', name='raw_facebook_hometown'),
	url(r'raw_facebook_interests', 'render.raw.interests', name='raw_facebook_interests'),
	url(r'raw_facebook_location', 'render.raw.locationfacebook', name='raw_facebook_location'),
	url(r'raw_facebook_political', 'render.raw.political', name='raw_facebook_political'),
	url(r'raw_facebook_religion', 'render.raw.religion', name='raw_facebook_religion'),
	url(r'raw_facebook_work', 'render.raw.work', name='raw_facebook_work'),	
	url(r'raw_questionnaire', 'render.raw.questionnaire', name='raw_questionnaire'),
	url(r'questionnaire_grouped_by_user', 'render.raw.questionnaire_grouped_by_user', name='questionnaire_grouped_by_user'),
	url(r'raw_users', 'render.raw.users', name='raw_users'),
	url(r'^about/', 'render.views.about', name='about'),
	url(r'data_quality', 'render.data_quality.data_quality', name='data_quality'),
	url(r'get_quality_users_for_period', 'render.data_quality.get_quality_users_for_period', name='get_quality_users_for_period'),
	url(r'^', 'render.views.home', name='home'),
)
