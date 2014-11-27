from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from .views import index, list_all, list, order

from .forms import AddProductForm, AddPackagingForm, AddPriceForm
from .views import AddProductWizard

from .forms import ModifyProductForm, ModifyPackagingForm, ModifyPriceForm
from .views import ModifyProductWizard, show_packaging_form, show_price_form


# add product wizard #
#forms
add_product_forms = [
        ('product'	, AddProductForm),
        ('packaging'	, AddPackagingForm),
        ('price'	, AddPriceForm),
]
#view
add_product_wizard = AddProductWizard.as_view(add_product_forms)
#wrapper with specific permissions
add_product_wrapper = permission_required('cms.BOARD',raise_exception=True)(add_product_wizard)


# modify product wizard #
#forms
modify_product_forms = [
        ('product'	, ModifyProductForm),
        ('packaging'	, ModifyPackagingForm),
        ('price'	, ModifyPriceForm),
]
#condition dict
modify_product_condition_dict = {
	'packaging'	: show_packaging_form,
	'price'		: show_price_form,
}
#view
modify_product_wizard = ModifyProductWizard.as_view(modify_product_forms, condition_dict=modify_product_condition_dict)
#wrapper with specific permissions
modify_product_wrapper = permission_required('cms.BOARD',raise_exception=True)(modify_product_wizard)

urlpatterns = patterns('',
  url(r'^$', index, name='index'),

  url(r'^add/$', add_product_wrapper, name='add'),

  url(r'^modify/(?P<product_id>.+?)/$', modify_product_wrapper, name='modify'),

  url(r'^list_all/$', list_all, name='list_all'),
  url(r'^list/(?P<product_id>.+?)/$', list, name='list'),

  url(r'^order/$', order, name='order'),

)
