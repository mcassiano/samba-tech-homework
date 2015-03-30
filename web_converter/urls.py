from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^$', views.UploadView.as_view(), name='upload_view'),
    url(r'^sign_s3$', views.sign_s3, name='sign_s3')
)