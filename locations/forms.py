# coding=utf-8

from django.forms import Form, ModelForm, Textarea, ModelChoiceField
from django.conf import settings

from .models import Location

#location form
class LocationForm(ModelForm):

  class Meta:
    model = Location
    fields = ( 'name', 'address', 'tel', 'email', 'website', 'contact', )
    widgets = {
      'address'         : Textarea(),
    }

#modify location wizard forms
class ListLocationsForm(Form):
  locations = ModelChoiceField(queryset=Location.objects.all())

