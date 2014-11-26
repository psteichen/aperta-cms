from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings

from django_tables2  import RequestConfig

from cms.functions import show_form

from .functions import gen_member_initial, gen_role_initial, gen_member_overview, gen_member_fullname
from .models import Member, Role
from .forms import MemberForm, RoleForm
from .tables  import MemberTable


# index #
#########
@permission_required('cms.BOARD')
def index(request):
  request.breadcrumbs( ( ('home','/'),
                         ('members','/members/'),
                        ) )

  return render(request, settings.TEMPLATE_CONTENT['members']['template'], {
                        'title': settings.TEMPLATE_CONTENT['members']['title'],
                        'actions': settings.TEMPLATE_CONTENT['members']['actions'],
                        })

# role_add #
############
@permission_required('cms.BOARD')
def role_add(r):
  r.breadcrumbs( ( ('home','/'),
                   ('members','/members/'),
                   ('add a role','/members/role/add/'),
                ) )

  if r.POST:
    rf = RoleForm(r.POST)
    if rf.is_valid():
      Rl = rf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['role']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['role']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['members']['role']['add']['done']['message'] + unicode(Rl),
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['role']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['role']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rf.errors]),
                })

  # no post yet -> empty form
  else:
    form = RoleForm()
    return render(r, settings.TEMPLATE_CONTENT['members']['role']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['role']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['role']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['role']['add']['submit'],
                'form': form,
                })


# add #
#######
@permission_required('cms.BOARD')
def add(r):
  r.breadcrumbs( ( ('home','/'),
                   ('members','/members/'),
                   ('add a member','/members/add/'),
                ) )

  if r.POST:
    mf = MemberForm(r.POST)
    if mf.is_valid():
      Me = mf.save(commit=False)
      Me.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['done']['title'], 
                'message': '',
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MemberForm()
    return render(r, settings.TEMPLATE_CONTENT['members']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['add']['submit'],
                'form': form,
                })


# modify #
##########

#modify helper functions
def show_role_form(wizard):
  return show_form(wizard,'member','role',True)

#modify formwizard
class ModifyMemberWizard(SessionWizardView):

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyMemberWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
         	                ('member','/members/'),
	               	        ('modify a member','/members/modify/'),
                            ) )

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['members']['modify']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['members']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['members']['modify']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['members']['modify'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['members']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyMemberWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'member':
      cleaned_data = self.get_cleaned_data_for_step('list') or {}
      if cleaned_data != {}:
        form.initial = gen_member_initial(cleaned_data['members'])
        form.instance = Member.objects.get(pk=cleaned_data['members'].id)

    if step == 'role':
      cleaned_data = self.get_cleaned_data_for_step('list') or {}
      if cleaned_data != {}:
        role = Role.objects.get(member=cleaned_data['members'].id)
        form.initial = gen_role_initial(role)
        form.instance = role

    return form

  def done(self, fl, **kwargs):
    self.request.breadcrumbs( ( ('home','/'),
         	                ('member','/members/'),
                	        ('modify a member','/members/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['members']['modify']['done']['template']

    M = R = None
    mf = fl[1]
    role = mf.cleaned_data['role']
    if role: rf = fl[2]

    if mf.is_valid():
      M = mf.save()

    if role: 
      if rf.is_valid():
        R = rf.save()

    title = settings.TEMPLATE_CONTENT['members']['modify']['done']['title'] % M

    return render(self.request, template, {
				'title': title,
                 })


# list #
#########
@permission_required('cms.BOARD')
def list(request):
  request.breadcrumbs( ( ('home','/'),
                         ('members','/members/'),
                         ('list members','/members/list/'),
                        ) )

  table = MemberTable(Member.objects.all().order_by('status', 'last_name'))
  RequestConfig(request, paginate={"per_page": 75}).configure(table)

  return render(request, settings.TEMPLATE_CONTENT['members']['list']['template'], {
                        'title': settings.TEMPLATE_CONTENT['members']['list']['title'],
                        'desc': settings.TEMPLATE_CONTENT['members']['list']['desc'],
                        'table': table,
                        })



# profile #
###########
@login_required
def profile(r, username):
  r.breadcrumbs( ( ('home','/'),
                   ('members','/members/'),
                   ('member profile','/members/profile/'),
               ) )

  member = Member.objects.get(user=r.user)
  title = settings.TEMPLATE_CONTENT['members']['profile']['title'] % { 'name' : gen_member_fullname(member), }
  message = gen_member_overview(settings.TEMPLATE_CONTENT['members']['profile']['overview']['template'],member)

  return render(r, settings.TEMPLATE_CONTENT['members']['profile']['template'], {
                   'title': title,
                   'message': message,
                })

