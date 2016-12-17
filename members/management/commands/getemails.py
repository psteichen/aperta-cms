import re

from django.core.management.base import BaseCommand, CommandError

from members.models import Member

class Command(BaseCommand):
  args = '<type>'
  help = 'Get list of member emails by status'

  def handle(self, *args, **options):
    out=''
    for ty in args:
      if ty == 'members':
        query =  Member.objects.filter(status=Member.ACT) | Member.objects.filter(status=Member.HON) | Member.objects.filter(status=Member.WBE)
      elif ty == 'board':
        query = Member.objects.filter(role__isnull=False)
      else:
        query = None

    if query is not None:
      for m in query:
        out += '"' + m.first_name + ' ' + m.last_name + '" <' + m.email + '>, '

    self.stdout.write(re.sub('\, $', '', out))
