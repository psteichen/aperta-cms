#
# coding=utf-8
#
from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings

from django_tables2  import RequestConfig

from .functions import gen_location_initial
from .models import Location
from .forms import LocationForm
from .tables  import LocationTable

#########
# VIEWS #
#########

# list #
########
@permission_required('cms.COMM',raise_exception=True)
def list(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('locations','/locations/'),
               ) )

  table = LocationTable(Location.objects.all().order_by('-id'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['locations']['template'], {
                   'title': settings.TEMPLATE_CONTENT['locations']['title'],
                   'actions': settings.TEMPLATE_CONTENT['locations']['actions'],
                   'table': table,
                })


# add #
#######
@permission_required('cms.COMM',raise_exception=True)
def add(r):
  r.breadcrumbs( ( ('home','/'),
                   ('locations','/locations/'),
                   ('add a location','/locations/add/'),
               ) )

  if r.POST:
    lf = LocationForm(r.POST)
    if lf.is_valid():
      Lo = lf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['locations']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['locations']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['locations']['add']['done']['message'] + unicode(Lo),
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['locations']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['locations']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in lf.errors]),
                })

  # no post yet -> empty form
  else:
    form = LocationForm()
    return render(r, settings.TEMPLATE_CONTENT['locations']['add']['template'], {
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

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
                                ('locations','/locations/'),
                                ('modify a location','/locations/modify/'),
                            ) )

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
    self.request.breadcrumbs( ( ('home','/'),
                                ('locations','/locations/'),
                                ('modify a location','/locations/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['locations']['modify']['done']['template']

    L = None
    lf = fl[1]
    if lf.is_valid():
      L = lf.save()

    title = settings.TEMPLATE_CONTENT['locations']['modify']['done']['title'] % L

    return render(self.request, template, {
                        'title': title,
                 })


# delete #
##########
@permission_required('cms.COMM',raise_exception=True)
def delete(r,location_id):
  r.breadcrumbs( ( 
			('home','/'),
                   	('locations','/locations/'),
                   	('delete a location','/locations/delete/'),
               ) )

  Lo = Location.objects.get(pk=location_id)
      
  # all fine -> done
  return render(r, settings.TEMPLATE_CONTENT['locations']['add']['done']['template'], {
               		'title': settings.TEMPLATE_CONTENT['locations']['add']['done']['title'], 
                	'message': settings.TEMPLATE_CONTENT['locations']['add']['done']['message'] + unicode(Lo),
               })


