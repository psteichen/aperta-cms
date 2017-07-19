#coding=utf-8

from django.forms import ModelForm, TextInput

from .models import BankExtract, BalanceSheet

#bank form
class BankExtractForm(ModelForm):

  class Meta:
    model = BankExtract
    fields = ( 'year', 'num', 'date', 'scan', ) 
    widgets = {
      'date'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
    }

#balance form
class BalanceSheetForm(ModelForm):

  class Meta:
    model = BalanceSheet
    fields = ( 'year', 'date', 'scan', ) 
    widgets = {
      'date'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
    }

