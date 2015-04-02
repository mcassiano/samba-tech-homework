from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
	url(r'^add_job$', views.add_job, name='add_job'),
    url(r'^get_status_on_job$', views.get_status_on_job, name='get_status_on_job'),
)