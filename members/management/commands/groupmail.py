import re
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail

from members.models import Member

class Command(BaseCommand):
  option_list = BaseCommand.option_list + (
	make_option('-f', '--from', dest='from',
            	help='Sender'),
	make_option('-g', '--group', dest='group',
            	help='GROUP to send message to', metavar='GROUP'),
	make_option('-s', '--subject', dest='subject',
            	help='Subject'),
	make_option('-m', '--message', dest='message',
            	help='Email message to send', metavar='MESSAGE'),
  	)

  def handle(self, *args, **options):
    query = None
    emails = ()

    # get members based on requested "group"
    self.stdout.write('''Groupmail from 
	<'''+options['from']+'''>
to group: <'''+options['group']+'''>''')

    if options['group'] == 'members':
      query =  Member.objects.filter(status=Member.ACT) | Member.objects.filter(status=Member.HON) | Member.objects.filter(status=Member.WBE)
    elif options['group'] == 'board':
      query = Member.objects.filter(role__isnull=False)
    else:
      query = None

    self.stdout.write('	'+str(query))

    # send(forward) mail to people of selected group
    if query is not None:
      for m in query:
        emails += (
	  (
          	options['subject'],
          	options['message'],
        	options['from'],
          	[m.email,],
	  ),
	)
        self.stdout.write('Prepared message for <'+str(m)+'>')

      self.stdout.write(''''Emails:
	'''+str(emails)+'''
''')

    send_mass_mail(emails)
    self.stdout.write('Emails sent!')



