from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^web_converter/', include('web_converter.urls')),
)
