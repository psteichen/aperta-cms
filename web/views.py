from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings

from django_tables2  import RequestConfig

from .models import Category
from .tables import CategoriesTable

# index #
#########
@permission_required('cms.COMM')
def list(request):
  request.breadcrumbs( ( 
				('home','/'),
                         	('web','/web/'),
                      ) )


  table = CategoriesTable(Category.objects.all())
  RequestConfig(request, paginate={"per_page": 75}).configure(table)

  return render(request, settings.TEMPLATE_CONTENT['web']['template'], {
                        'title': settings.TEMPLATE_CONTENT['web']['title'],
                        'actions': settings.TEMPLATE_CONTENT['web']['actions'],
                        'table': table,
                        })


