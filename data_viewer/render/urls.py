from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'test', 'render.views.test', name='test'),
	url(r'raw_phone_location', 'render.raw.location', name='raw_phone_location'),
	url(r'^', 'render.views.home', name='home'),
)
