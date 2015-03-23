from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from .views import list, add, delete
from .forms import LocationForm, ContactForm
from .views import ModifyLocationWizard, show_contact_form

# modify location wizard #
#forms
modify_location_forms = [
        ('location'	, LocationForm),
        ('contact'	, ContactForm),
]
#condition dict
modify_condition_dict = {
        'contact'      : show_contact_form,
}
modify_location_wizard = ModifyLocationWizard.as_view(modify_location_forms, condition_dict=modify_condition_dict)
#wrapper with specific permissions
modify_location_wrapper = permission_required('cms.COMM',raise_exception=True)(modify_location_wizard)


urlpatterns = patterns('',
  url(r'^$', list, name='list'),

  url(r'^add/$', add, name='add'),
  url(r'^modify/(?P<location_id>\d+)/$', modify_location_wrapper, name='modify'),
  url(r'^delete/(?P<location_id>\d+)/$', delete, name='delete'),
)
