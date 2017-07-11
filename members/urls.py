from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from .views import list, add, modify
from .views import roles, r_add, r_modify, r_type
from .views import profile, p_modify


urlpatterns = patterns('',
  url(r'^$', list, name='list'),
  url(r'^add/', add, name='add'),
#  url(r'^modify/(?P<mem_id>.+?)/$', modify_member_wrapper, name='modify'),
  url(r'^modify/(?P<mem_id>.+?)/$', modify, name='modify'),

  url(r'^roles/$', roles, name='roles'),
  url(r'^roles/add/$', r_add, name='roles_add'),
  url(r'^roles/modify/(?P<role_id>.+?)/$', r_modify, name='roles_modify'),
  url(r'^roles/type/$', r_type, name='roles_type'),

  url(r'^profile/modify/(?P<username>.+?)/$', p_modify, name='profile_modify'),
  url(r'^profile/(?P<username>.+?)/$', profile, name='profile'),
)
