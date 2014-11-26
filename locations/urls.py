from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from .views import index, add, list
from .forms import ListLocationsForm, LocationForm
from .views import ModifyLocationWizard

# modify location wizard #
#forms
modify_location_forms = [
        ('list'         , ListLocationsForm),
        ('location'	, LocationForm),
]
#view
modify_location_wizard = ModifyLocationWizard.as_view(modify_location_forms)
#wrapper with specific permissions
modify_location_wrapper = permission_required('cms.COMM',raise_exception=True)(modify_location_wizard)


urlpatterns = patterns('',
  url(r'^$', index, name='index'),

  url(r'^add/$', add, name='add'),
  url(r'^modify/$', modify_location_wrapper, name='modify'),
  url(r'^list/$', list, name='list'),
)
