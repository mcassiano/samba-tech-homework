from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('web_converter.urls')),
    url(r'^encoder/', include('encoder.urls')),
    url(r'^uploader/', include('uploader.urls')),
)
