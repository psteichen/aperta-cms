#
# coding=utf-8
#
from datetime import date, timedelta

from django.template.response import TemplateResponse
from django.conf import settings

from django_tables2  import RequestConfig
from formtools.wizard.views import SessionWizardView

from headcrumbs.decorators import crumb
from headcrumbs.util import name_from_pk

from cms.functions import group_required

from .functions import gen_location_initial
from .models import Location
from .forms import LocationForm
from .tables  import LocationTable, MgmtLocationTable

#########
# VIEWS #
#########

# list #
########
@group_required('MEMBER')
@crumb(u'Lieux de Rencontres')
def list(r):

  table = LocationTable(Location.objects.all().order_by('-id'))
  if r.user.has_perm('cms.COMM'):
    table = MgmtLocationTable(Location.objects.all().order_by('-id'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['locations']['template'], {
                   'title': settings.TEMPLATE_CONTENT['locations']['title'],
                   'actions': settings.TEMPLATE_CONTENT['locations']['actions'],
                   'table': table,
                })


# add #
#######
@group_required('BOARD')
@crumb(u'Ajouter un lieux',parent=list)
def add(r):

  if r.POST:
    lf = LocationForm(r.POST)
    if lf.is_valid():
      Lo = lf.save()
      
      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['locations']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['locations']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['locations']['add']['done']['message'] + unicode(Lo),
                })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['locations']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['locations']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in lf.errors]),
                })

  # no post yet -> empty form
  else:
    form = LocationForm()
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['locations']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['locations']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['locations']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['locations']['add']['submit'],
                'form': form,
                })

# modify formwizard #
#####################
class ModifyLocationWizard(SessionWizardView):

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyLocationWizard, self).get_context_data(form=form, **kwargs)

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['locations']['modify']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['locations']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['locations']['modify']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['locations']['modify'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['locations']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyLocationWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'location':
      cleaned_data = self.get_cleaned_data_for_step('list') or {}
      if cleaned_data != {}:
        form.initial = gen_location_initial(cleaned_data['locations'])
        form.instance = Location.objects.get(pk=cleaned_data['locations'].id)

    return form

  def done(self, fl, **kwargs):

    template = settings.TEMPLATE_CONTENT['locations']['modify']['done']['template']

    L = None
    lf = fl[1]
    if lf.is_valid():
      L = lf.save()

    title = settings.TEMPLATE_CONTENT['locations']['modify']['done']['title'] % L

    return TemplateResponse(self.request, template, {
                        'title': title,
                 })


# delete #
##########
@group_required('BOARD')
def delete(r,location_id):

  Lo = Location.objects.get(pk=location_id)
      
  # all fine -> done
  return TemplateResponse(r, settings.TEMPLATE_CONTENT['locations']['add']['done']['template'], {
               		'title': settings.TEMPLATE_CONTENT['locations']['add']['done']['title'], 
                	'message': settings.TEMPLATE_CONTENT['locations']['add']['done']['message'] + unicode(Lo),
               })


