# coding=utf-8

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, IntegerField
from django.forms.models import modelformset_factory, BaseModelFormSet

from .models import Product, Packaging, Price, Order

#add forms
class AddProductForm(ModelForm):

  class Meta:
    model = Product
    fields = ( 'title', 'desc', 'image', )

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

  class Meta:
    model = Order
    fields = ( 'product', 'amount', )
    labels = {
      'product'		: u'Produit(s)',
      'amount'		: u'Quantité',
    }
    widgets = {
      'product'		: TextInput(attrs={'readonly': 'readlonly', 'size': 50}),
    }

OrderModelFormSet = modelformset_factory(Order, form=OrderForm, formset=BaseModelFormSet)

