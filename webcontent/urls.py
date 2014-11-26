from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .views import index, add_page, list_pages
from .forms import ListPagesForm, ModifyPageForm
from .views import ModifyPageWizard

# modify page wizard #
#forms
modify_page_forms = [
        ('list'         , ListPagesForm),
        ('page'		, ModifyPageForm),
]
#view
modify_page_wizard = ModifyPageWizard.as_view(modify_page_forms)
#wrapper with specific permissions
modify_page_wrapper = login_required(modify_page_wizard)


from .views import index, add_category, list_categories
from .forms import ListCategoriesForm, ModifyCategoryForm
from .views import ModifyCategoryWizard

# modify category wizard #
#forms
modify_category_forms = [
        ('list'         , ListCategoriesForm),
        ('category'	, ModifyCategoryForm),
]
#view
modify_category_wizard = ModifyCategoryWizard.as_view(modify_category_forms)
#wrapper with specific permissions
modify_category_wrapper = login_required(modify_category_wizard)


urlpatterns = patterns('',
  url(r'^$', index, name='index'),

  url(r'^page/add/$', add_page, name='add_page'),
  url(r'^page/modify/$', modify_page_wrapper, name='modify_page'),
  url(r'^page/list/$', list_pages, name='list_pages'),

  url(r'^category/add/$', add_category, name='add_category'),
  url(r'^category/modify/$', modify_category_wrapper, name='modify_category'),
  url(r'^category/list/$', list_categories, name='list_categories'),

)
