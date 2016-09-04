from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django_tables2  import RequestConfig

from .forms import ImportData


# upload #
##########
@permission_required('cms.BOARD')
def upload(r,ty):
  r.breadcrumbs( ( 	
			('home','/'),
                   	('import data','/upload/'+ty+'/'),
               ) )

  template  	= settings.TEMPLATE_CONTENT['upload'][ty]['template']
  title  	= settings.TEMPLATE_CONTENT['upload'][ty]['title']
  desc      	= settings.TEMPLATE_CONTENT['upload'][ty]['desc']
  submit    	= settings.TEMPLATE_CONTENT['upload'][ty]['submit']

  done_template  = settings.TEMPLATE_CONTENT['upload'][ty]['done']['template']
  done_title     = settings.TEMPLATE_CONTENT['upload'][ty]['done']['title']
  done_message   = settings.TEMPLATE_CONTENT['upload'][ty]['done']['message']

  if r.POST:
    idf = ImportData(r.POST, r.FILES)
    if idf.is_valid():
      data      = idf.cleaned_data['data']

      # handle uploaded file
      errors = import_data(ty,data)

      if errors:
        # issue with import -> error
        return render(r, done_template, {
                               'title'          : done_title,
                               'error_message'  : settings.TEMPLATE_CONTENT['error']['gen'] + str(errors),
                    })

      # all fine -> done
      return render(r, done_template, {
                               'title'    : done_title,
                               'message'  : done_message,
                  })

    else:
      # form not valid -> error
      return render(r, done_template, {
                               'title'          : done_title,
                               'error_message'  : settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in idf.errors]),
                  })

  else:
    # no post yet -> empty form
    form = ImportData()
    return render(r, template, {
                             'title'    : title,
                             'desc'     : desc,
                             'submit'   : submit,
                             'form'     : form,
                })


