#
# coding=utf-8
#
from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings

from django_tables2  import RequestConfig

from cms.functions import show_form

from .functions import gen_location_initial, gen_contact_initial
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

  table = LocationTable(Location.objects.all())
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
def show_contact_form(wiz):
  return show_form(wiz,'location','ct',True)

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
      context.update({'title': settings.TEMPLATE_CONTENT['locations']['modify'][self.steps.current]['title']})
      context.update({'desc': settings.TEMPLATE_CONTENT['locations']['modify'][self.steps.current]['desc']})
      context.update({'first': settings.TEMPLATE_CONTENT['locations']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['locations']['modify']['prev']})
      context.update({'next': settings.TEMPLATE_CONTENT['locations']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyLocationWizard, self).get_form(step, data, files)

    L = Location.objects.get(pk=self.kwargs['location_id'])

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'location':
      form.initial = gen_location_initial(L)
      form.instance = L

    if step == 'contact':
      if L.contact:
        form.initial = gen_contact_initial(L.contact)
        form.instance = L.contact

    return form

  def done(self, fl, form_dict, **kwargs):
    self.request.breadcrumbs( ( ('home','/'),
                                ('locations','/locations/'),
                                ('modify a location','/locations/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['locations']['modify']['done']['template']

    L = C = None
    lf = form_dict['location']

    contact = lf.cleaned_data['ct']
    if contact:
      cf = form_dict['contact']
      if cf.is_valid():
        C = cf.save()

    if lf.is_valid():
      L = lf.save(commit=False)
      if contact:
        L.contact = C
      L.save()

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


