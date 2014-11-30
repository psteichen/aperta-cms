# coding=utf-8

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, ModelMultipleChoiceField, CheckboxSelectMultiple, IntegerField
from django.db.models import modelformset_factory, BaseModelFormSet

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
class OrderForm(ModelForm):
  product	= CharField(label=u'Produit(s)',widget=TextInput(attrs={'readonly', 'size': 50}))
  amount	= IntegerField(label=u'Quantité')

  class Meta:
    model = Order

MultiOrderModelFormSet = modelformset_factory(Order, form=OrderForm, formset=BaseModelFormSet)

