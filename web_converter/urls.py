from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^$', views.upload_view, name='upload_view'),

    url(r'^(?P<identifier>[a-zA-Z0-9_.-]+)/$',
        views.video_detail, name='video_detail'),

    url(r'^save_video_details$', views.save_video_details, 
    	name='save_video_details'),
   
)