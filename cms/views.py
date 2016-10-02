
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

################
# GLOBAL VIEWS #
################
@login_required
def home(request):
  return render(request, settings.TEMPLATE_CONTENT['home']['template'], { 'actions': settings.TEMPLATE_CONTENT['home']['actions'], })

