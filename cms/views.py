
from headcrumbs.decorators import crumb

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


################
# GLOBAL VIEWS #
################
@login_required
@crumb(u'Accueil')
def home(request):
  return render(request, settings.TEMPLATE_CONTENT['home']['template'], { 'actions': settings.TEMPLATE_CONTENT['home']['actions'], })

