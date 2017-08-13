from django.conf.urls import url

from .views import init

urlpatterns = [
  url(r'^$', init, name='init'),
]
