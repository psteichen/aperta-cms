from django.conf.urls import include, url
from django.contrib.auth.decorators import permission_required

from .views import list, add, delete
from .forms import LocationForm, ContactForm
from .views import ModifyLocationWizard

# modify location wizard #
#forms
modify_location_forms = [
        ('location'	, LocationForm),
        ('contact'	, ContactForm),
]
#view
modify_location_wizard = ModifyLocationWizard.as_view(modify_location_forms)
#wrapper with specific permissions
modify_location_wrapper = permission_required('cms.COMM',raise_exception=True)(modify_location_wizard)


urlpatterns = [
  url(r'^$', list, name='list'),

  url(r'^add/$', add, name='add'),
  url(r'^modify/(?P<location_id>.+?)$', modify_location_wrapper, name='modify'),
  url(r'^delete/(?P<location_id>.+?)$', delete, name='delete'),
]
