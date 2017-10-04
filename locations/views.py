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


# modify #
##########
@group_required('BOARD')
def modify(r,location_id):

  Lo = Location.objects.get(pk=location_id)

  template	= settings.TEMPLATE_CONTENT['locations']['modify']['template'] 
  title 	= settings.TEMPLATE_CONTENT['locations']['modify']['title'].format(location=unicode(Lo))
  desc		= settings.TEMPLATE_CONTENT['locations']['add']['desc']
  submit	= settings.TEMPLATE_CONTENT['locations']['add']['submit']

  done_template	= settings.TEMPLATE_CONTENT['locations']['modify']['done']['template']
  done_title	= settings.TEMPLATE_CONTENT['locations']['modify']['done']['title'].format(location=unicode(Lo)) 
  done_message	= settings.TEMPLATE_CONTENT['locations']['modify']['done']['message'].format(location=unicode(Lo))

      
  if r.POST:
    lf = LocationForm(r.POST,instance=Lo)
    if lf.is_valid():
      L = lf.save()
      
      # all fine -> done
      return TemplateResponse(r, done_template, {
	                	'title'		: done_title, 
        	     		'message'	: done_message,
                	    })

    # form not valid -> error
    else:
      return TemplateResponse(r, done_template, {
		                'title'		: done_title, 
                		'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in lf.errors]),
                	    })

  # no post yet -> empty form
  else:
    form = LocationForm()
    form.initial = gen_location_initial(Lo)
    form.instance = Lo

    return TemplateResponse(r, template, {
		                'title'		: title,
                		'desc'		: desc,
              			'submit'	: submit,
                		'form'		: form,
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


