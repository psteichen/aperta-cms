import re

from django.core.management.base import BaseCommand, CommandError

from cms.functions import getSaison

from members.models import Member, Role

class Command(BaseCommand):
  help = 'Get list of member emails by status'

  def add_arguments(self, parser):
    parser.add_argument('args', metavar='group', nargs='+')

  def handle(self, *groups, **options):
    out=''
    query = None

    # get members based on requested "group"
    for g in groups:
      if g == 'all':
        query =  Member.objects.filter(status=Member.ACT) | Member.objects.filter(status=Member.HON) | Member.objects.filter(status=Member.WBE) | Member.objects.filter(status=Member.STB)
      if g == 'members':
        query =  Member.objects.filter(status=Member.ACT) | Member.objects.filter(status=Member.WBE)
      elif g == 'board':
        query = Member.objects.filter(role__year=getSaison())
#        query = Role.objects.filter(year=getSaison()).values('member')
      else:
        query = None

    # create list of emails for "group"
    if query is not None:
      for m in query:
        out += '"' + m.first_name + ' ' + m.last_name + '" <' + m.email + '>, '

    self.stdout.write(self.style.SUCCESS(re.sub('\, $', '', out)))
