# encoding=utf-8 #
 
from django.conf import settings
from django.forms import Form, FileField, ChoiceField

TYPES = (
  ( 'MEMBER',	u'Liste de members'),
  ( 'MEETING',	u'Calendrier des réunions'),
)

#form to import data
class ImportData(Form):
  ty  	= ChoiceField(choices=TYPES)
  data 	= FileField()
