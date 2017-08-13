from django.conf.urls import include, url

from .views import upload

urlpatterns = [
  url(r'^(?P<ty>.+?)/', upload, name='upload'),
]
