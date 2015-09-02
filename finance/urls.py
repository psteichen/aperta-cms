from django.conf.urls import patterns, url

#from .views import list, invoice, payment, bank
from .views import bank, upload

urlpatterns = patterns('',
#  url(r'^$', list, name='list'),

#  url(r'^invoice/', invoice, name='invoice'),
#  url(r'^invoice/(?P<id>.+?)/$', invoice, name='invoice'),

#  url(r'^payment/', payment, name='payment'),
#  url(r'^payment/(?P<id>.+?)/$', payment, name='payment'),

  url(r'^bank/$', bank, name='bank'),
  url(r'^bank/upload/$', upload, name='upload'),
  url(r'^bank/(?P<ynum>.+?)/$', bank, name='bank'),

)
