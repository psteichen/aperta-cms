import re

from django.core.management.base import BaseCommand, CommandError

from members.models import Member

class Command(BaseCommand):
  args = '<group>'
  help = 'Get list of member emails by status'

  def handle(self, *args, **options):
    out=''
    query = None

    # get members based on requested "group"
    for ty in args:
      if ty == 'all':
        query =  Member.objects.all()
      if ty == 'members':
        query =  Member.objects.filter(status=Member.ACT) | Member.objects.filter(status=Member.HON) | Member.objects.filter(status=Member.WBE)
      elif ty == 'board':
        query = Member.objects.filter(role__isnull=False)
      else:
        query = None

    # create list of emails for "group"
    if query is not None:
      for m in query:
        out += '"' + m.first_name + ' ' + m.last_name + '" <' + m.email + '>, '

    self.stdout.write(re.sub('\, $', '', out))
