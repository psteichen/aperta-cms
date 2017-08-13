from django.conf.urls import url

#from .views import invoice, payment
from .views import list, bank, balance, upload

urlpatterns = [
  url(r'^$', list, name='list'),

#  url(r'^invoice/', invoice, name='invoice'),
#  url(r'^invoice/(?P<id>.+?)/$', invoice, name='invoice'),

#  url(r'^payment/', payment, name='payment'),
#  url(r'^payment/(?P<id>.+?)/$', payment, name='payment'),

  url(r'^bank/$', bank, name='bank'),
  url(r'^bank/(?P<ynum>.+?)/$', bank, name='bank'),

  url(r'^balance/$', balance, name='balance'),
  url(r'^balance/(?P<year>.+?)/$', balance, name='balance'),

  url(r'^upload/(?P<ty>.+?)/$', upload, name='upload'),

]
