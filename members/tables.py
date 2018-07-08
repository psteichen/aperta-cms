#coding=utf-8

from datetime import date

from django.conf import settings
from django_tables2.tables import Table
from django_tables2 import Column, LinkColumn
from django_tables2.utils import A

from django.utils.safestring import mark_safe
from django.utils.html import escape

from cms.functions import getSaison

from attendance.models import Meeting_Attendance

from .models import Member, Role


def view_modal(member,roles):
  modal = u'''
<!-- Modal -->
<div class="modal fade" id="{id}Modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">{name} <span class="badge">Rôle(s): {roles}</span></h4>
      </div> 
      <div class="modal-body">
        <center><img src="{pic}" alt="Photo" class="img-responsive img-rounded" /></center>
        <strong>Email :</strong> <p>{email}</p>
        <strong>Tél. fixe :</strong> <p>{phone}</p>
        <strong>Mobile :</strong> <p>{mobile}</p>
      </div>
    </div>
  </div>
</div>
'''.format(id=member.pk,name=str(member),pic=settings.MEDIA_URL+str(member.photo),email=str(member.email),phone=str(member.phone),mobile=str(member.mobile),roles=roles)

  return modal 


#table for visualisation via django_tables2
class MemberTable(Table):
  role          = Column(verbose_name=u'Rôle(s) ['+getSaison()+'] ',empty_values=())
  meetings    	= Column(verbose_name=u'RS (présent / excusé)',empty_values=())
  view		= Column(verbose_name=u'Visualiser',empty_values=())

  def __init__(self, *args, **kwargs):
    if kwargs["username"]:
      self.username = kwargs["username"]
      kwargs.pop('username',False)
    super(Table, self).__init__(*args, **kwargs)

  def render_photo(self, value, record):
    roles = u''
    try:
      R = Role.objects.filter(member__id=record.id,year=getSaison())
      for r in R:
        roles += str(r.type.title)
        if r != R.last(): roles += u' ; '
    except Role.DoesNotExist:
      pass

    picture = u'<i class="fa-stack"><a href="#{id}Modal" data-toggle="modal"><img src="{pic}" alt="Photo" class="img-responsive img-circle" /></a></i>'.format(id=record.pk,pic=settings.MEDIA_URL+str(value)) + view_modal(record,roles)

    return mark_safe(picture)

  def render_last_name(self, value):
    return str.upper(value)

  def render_role(self, value, record):
    roles = u''
    try:
      R = Role.objects.filter(member__id=record.id,year=getSaison())
      for r in R:
        roles += str(r.type.title)
        if r != R.last(): roles += u' ; '
      return roles
    except Role.DoesNotExist:
      return ''

  def render_meetings(self, record):
    MA = Meeting_Attendance.objects.filter(member=record)
    ma = ' {} / {} '.format(MA.filter(present=True).count(),MA.filter(present=False).count())
    return mark_safe(ma)

  def render_view(self, record):
    roles = u''
    try:
      R = Role.objects.filter(member__id=record.id,year=getSaison())
      for r in R:
        roles += str(r.type.title)
        if r != R.last(): roles += u' ; '
    except Role.DoesNotExist:
      pass

#    link = u'<a class="btn btn-info btn-sm" href="#{id}Modal" data-toggle="modal"><i class="fa fa-eye"></i></a>'.format(id=record.pk) + view_modal(record,roles)
    link = u'<a class="btn btn-info btn-sm" href="/members/profile/#{user}/"><i class="fa fa-eye"></i></a>'.format(user=record.user)

    mod = ''
    if self.username == record.user.username: 
      mod = '<a class="btn btn-danger btn-sm pull-right" href="/members/profile/modify/{}/"><i class="fa fa-pencil"></i></a>'.format(escape(record.user))

    return mark_safe(link + mod)

  class Meta:
    model = Member
    fields = ( 'photo', 'first_name', 'last_name', 'email', 'mobile', 'status', 'role', 'meetings', )
    attrs = {"class": "table table-striped"}

#management table
class MgmtMemberTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  role          = Column(verbose_name=u'Rôle(s) ['+getSaison()+'] ',empty_values=())
  meetings    	= Column(verbose_name=u'RS (présent / excusé)',empty_values=())
  view		= Column(verbose_name=u'Visualiser',empty_values=())
  modify	= Column(verbose_name=u'Modifier',empty_values=())

  def render_row_class(self, value, record):
    cl = ''
    if record.status == Member.ACT:
      cl = 'success'
    if record.status == Member.WBE:
      cl = 'info'

    att = record.attendance.all().count()
    exc = record.excused.all().count()
    if att == 0:
      cl = 'warning'
    if record.end_date or record.status == Member.STB or (att == 0 and exc == 0):
      cl = 'danger'

    return cl

  def render_photo(self, value, record):
    roles = u''
    try:
      R = Role.objects.filter(member__id=record.id,year=getSaison())
      for r in R:
        roles += str(r.type.title)
        if r != R.last(): roles += u' ; '
    except Role.DoesNotExist:
      pass

    picture = u'<i class="fa-stack"><a href="#{id}Modal" data-toggle="modal"><img src="{pic}" alt="Photo" class="img-responsive img-circle"/></a></i>'.format(id=record.pk,pic=settings.MEDIA_URL+str(value)) + view_modal(record,roles)

    return mark_safe(picture)

  def render_last_name(self, value):
    return str.upper(value)

#  def render_start_date(self, value):
#    return format_datetime(value)

#  def render_end_date(self, value):
#    return format_datetime(value)

  def render_role(self, value, record):
    roles = u''
    try:
      R = Role.objects.filter(member__id=record.id,year=getSaison())
      for r in R:
        roles += str(r.type.title)
        if r != R.last(): roles += u' ; '
      return roles
    except Role.DoesNotExist:
      return ''

  def render_meetings(self, record):
    MA = Meeting_Attendance.objects.filter(member=record)
    return '{} / {}'.format(MA.filter(present=True).count(),MA.filter(present=False).count())

  def render_view(self, record):
    roles = u''
    try:
      R = Role.objects.filter(member__id=record.id,year=getSaison())
      for r in R:
        roles += str(r.type.title)
        if r != R.last(): roles += u' ; '
    except Role.DoesNotExist:
      pass

#    link = u'<a class="btn btn-info btn-sm" href="#{id}Modal" data-toggle="modal"><i class="fa fa-eye"></i></a>'.format(id=record.pk) + view_modal(record,roles)
    link = u'<a class="btn btn-info btn-sm" href="/members/profile/{user}/"><i class="fa fa-eye"></i></a>'.format(user=record.user)

    return mark_safe(link)

  def render_modify(self, record):
    link = '<a class="btn btn-danger btn-sm" href="/members/modify/{}/"><i class="fa fa-pencil"></i></a>'.format(escape(record.pk))
    return mark_safe(link)


  class Meta:
    model = Member
    fields = ( 'photo', 'first_name', 'last_name', 'email', 'mobile', 'status', 'role', 'meetings', )
    attrs = {"class": "table table-striped"}

#roles table
class RoleTable(Table):
  modify      = Column(verbose_name=u'Modifier',empty_values=())

  def render_modify(self, record):
    link = '<a class="btn btn-danger btn-sm" href="/members/roles/modify/{}/"><i class="fa fa-pencil"></i></a>'.format(escape(record.pk))
    return mark_safe(link)

  class Meta:
    model = Role
    fields = ( 'year', 'type', 'member', )
    attrs = {"class": "table table-striped"}

