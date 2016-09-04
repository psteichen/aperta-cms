from django.conf.urls import patterns, include, url

from .views import upload

urlpatterns = patterns('',
  url(r'^(?P<ty>.+?)/', upload, name='upload'),
)
