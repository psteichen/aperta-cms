from django.conf import settings

def template_content(request):
    return settings.TEMPLATE_CONTENT

def group_perms(request):
  if request.user.is_authenticated():
    gl = request.user.groups.all().values_list('name', flat=True)
  else:
    gl = False

  return {
    'groups': gl
  }
