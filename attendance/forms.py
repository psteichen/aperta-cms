# coding=utf-8

from django.forms import Form, ModelMultipleChoiceField, CheckboxSelectMultiple

from members.functions import get_active_members

#used in modify meeting and modify event form wizards
class ModifyAttendanceForm(Form):
  subscribed	= ModelMultipleChoiceField(label=u'Présent',queryset=get_active_members(),widget=CheckboxSelectMultiple,required=False)
  excused	= ModelMultipleChoiceField(label=u'Excusé',queryset=get_active_members(),widget=CheckboxSelectMultiple,required=False)

