import re

from django.core.management.base import BaseCommand, CommandError

from members.models import Member

class Command(BaseCommand):
  args = '<type>'
  help = 'Get list of member emails by status'

  def handle(self, *args, **options):
    out=''
    for ty in args:
      for m in Member.objects.filter(status=ty):
        out += '"' + m.first_name + ' ' + m.last_name + '" <' + m.email + '>, '

    self.stdout.write(re.sub('\, $', '', out))
