from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from .forms import ListMembersForm, ModifyMemberForm, ModifyRoleForm, RoleForm
from .views import ModifyMemberWizard, show_mod_role_form, show_add_role_form
from .views import list, profile, add, upload
from .views import role_add

# modify wizard #
#forms
modify_member_forms = [
        ('member'       , ModifyMemberForm),
        ('mod_role'     , ModifyRoleForm),
        ('add_role'     , RoleForm),
]
#condition dict
modify_member_condition_dict = {
	'mod_role'	: show_mod_role_form,
	'add_role'	: show_add_role_form,
}

#view
modify_member_wizard = ModifyMemberWizard.as_view(modify_member_forms, condition_dict=modify_member_condition_dict)
#wrapper with specific permissions
modify_member_wrapper = permission_required('cms.BOARD',raise_exception=True)(modify_member_wizard)

urlpatterns = patterns('',
  url(r'^$', list, name='list'),
  url(r'^add/', add, name='add'),
  url(r'^import/$', upload, name='import'),
  url(r'^role/add/', role_add, name='role_add'),
  url(r'^modify/(?P<mem_id>.+?)/$', modify_member_wrapper, name='modify'),

  url(r'^profile/(?P<username>.+?)', profile, name='profile'),
)
