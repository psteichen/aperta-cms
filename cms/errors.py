from django.shortcuts import render
from django.conf import settings


################
# ERROR VIEWS #
################
def http_error(request,code):
  return render(request, settings.TEMPLATE_CONTENT['error'][code]['template'], {'user': request.user})

def code400(r):
  return http_error(r,400)
def code403(r):
  return http_error(r,403)
def code404(r):
  return http_error(r,404)
def code500(r):
  return http_error(r,500)
