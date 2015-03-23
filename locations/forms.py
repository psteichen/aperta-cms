# coding=utf-8

from django.forms import Form, ModelForm, Textarea, ModelChoiceField
from django.conf import settings

from .models import Location, Contact

#location form
class LocationForm(ModelForm):

  class Meta:
    model = Location
    fields = ( 'name', 'address', 'tel', 'email', 'website', 'contact', )
    widgets = {
      'address'         : Textarea(),
    }

class ContactForm(ModelForm):

  class Meta:
    model = Contact
    fields = ( 'first_name', 'last_name', 'tel', 'mobile', 'email', )

