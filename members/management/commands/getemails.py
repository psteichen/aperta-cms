import re

from django.core.management.base import BaseCommand, CommandError

from members.models import Member

class Command(BaseCommand):
  help = 'Get list of member emails by status'

  def add_arguments(self, parser):
    parser.add_argument('args', metavar='group', nargs='+')

  def handle(self, *groups, **options):
    out=''
    query = None

    # get members based on requested "group"
    for g in groups:
      if g == 'members':
        query =  Member.objects.filter(status=Member.ACT) | Member.objects.filter(status=Member.HON) | Member.objects.filter(status=Member.WBE)
      elif g == 'board':
        query = Member.objects.filter(role__isnull=False)
      else:
        query = None

    # create list of emails for "group"
    if query is not None:
      for m in query:
        out += '"' + m.first_name + ' ' + m.last_name + '" <' + m.email + '>, '

    self.stdout.write(self.style.SUCCESS(re.sub('\, $', '', out)))
