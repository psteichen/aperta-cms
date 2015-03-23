# coding=utf-8

from datetime import date

from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField
from django.conf import settings

from .models import Meeting, Location

#location form
class LocationForm(ModelForm):

  class Meta:
    model = Location
    fields = ( 'name', 'address', )
    widgets = {
      'address'         : Textarea(),
    }

#modify location wizard forms
class ListLocationsForm(Form):
  locations = ModelChoiceField(queryset=Location.objects.all())


#meeting form
class MeetingForm(ModelForm):
  additional_message 	= CharField(label='Message supplémentaire',widget=Textarea(attrs={'placeholder': "Message à transmettre dans l'invitation.",}),required=False)
  send 			= BooleanField(label='Envoi direct des invitations',required=False)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'time', 'location', 'num', 'deadline', 'additional_message', 'send', )
    widgets = {
#      'title'	: TextInput(attrs={'readonly': 'readonly', }),
      'when'	: TextInput(attrs={'type': 'date', }),
      'time'	: TextInput(attrs={'type': 'time', }),
      'deadline': TextInput(attrs={'type': 'date', }),
      'num'	: HiddenInput(),
    }


#modify wizard forms
class ListMeetingsForm(Form):
  meetings = ModelChoiceField(queryset=Meeting.objects.all().order_by('-num'))

class ModifyMeetingForm(ModelForm):

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'time', 'location', 'attendance', 'excused', )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', }),
      'time'	: TextInput(attrs={'type': 'time', }),
    }


