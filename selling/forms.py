# coding=utf-8

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, MultipleModelChoiceField, CheckboxSelectMultiple, IntegerField

from .models import Product, Packaging, Price, Order

#add forms
class AddProductForm(ModelForm):

  class Meta:
    model = Product
    fields = ( 'title', 'desc', )

class AddPackagingForm(ModelForm):

  class Meta:
    model = Packaging
    fields = ( 'desc', 'content', 'units',  )

class AddPriceForm(ModelForm):

  class Meta:
    model = Price
    fields = ( 'buying', 'selling',  )


#order forms
class SelectProductForm(Form):
  products	= MultipleModelChoiceField(queryset=Product.objects.all(),widget=CheckboxSelectMultiple)

class AmountForm(Form):
  amount	= IntegerField()

