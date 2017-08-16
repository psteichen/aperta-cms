#
# coding=utf-8
#
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.conf import settings

from headcrumbs.decorators import crumb

from .functions import group_required, check_if_setup


################
# GLOBAL VIEWS #
################
@group_required('MEMBER')
@crumb(u'Accueil')
def home(request):
  if not check_if_setup():  return TemplateResponse(request, settings.TEMPLATE_CONTENT['home']['template'], { 'actions': settings.TEMPLATE_CONTENT['home']['actions'], 'alert': settings.TEMPLATE_CONTENT['home']['setup_alert'], })
  return TemplateResponse(request, settings.TEMPLATE_CONTENT['home']['template'], { 'actions': settings.TEMPLATE_CONTENT['home']['actions'], })

