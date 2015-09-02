#coding=utf-8

from django.forms import ModelForm, TextInput

from .models import BankExtract

#bank form
class BankExtractForm(ModelForm):

  class Meta:
    model = BankExtract
    fields = ( 'year', 'num', 'scan', ) 
    widgets = {
      'start_date'	: TextInput(attrs={'type': 'date', 'id': 'ypicker', }),
    }

