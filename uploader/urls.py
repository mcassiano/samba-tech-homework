from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^get_signed_s3_url$', views.get_signed_s3_url,
    	name='get_signed_s3_url'),
)