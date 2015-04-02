from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^$', views.upload_view, name='upload_view'),
    url(r'^sign_s3$', views.sign_s3, name='sign_s3'),

    url(r'^(?P<identifier>[a-zA-Z0-9_.-]+)/$',
        views.video_detail, name='video_detail'),

    url(r'^save_video_details$', views.save_video_details, 
    	name='save_video_details'),
    
    url(r'^add_job$', views.add_job, name='add_job'),
    url(r'^get_status_on_job$', views.get_status_on_job, name='get_status_on_job')
)