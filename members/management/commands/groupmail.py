import re
import email
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail, EmailMessage
from django.db.models import Q

from members.models import Member

class Command(BaseCommand):
  option_list = BaseCommand.option_list + (
	make_option('-f', '--from', dest='from',
            	help='Sender'),
	make_option('-g', '--group', dest='group',
            	help='GROUP to send message to', metavar='GROUP'),
	make_option('-m', '--message', dest='message',
            	help='Email message to send', metavar='MESSAGE'),
  	)

  def handle(self, *args, **options):
    query = None
    message = None
    subject = '[FIFTY-ONE APERTA - ' + str.upper(str(options['group'])) + '] '
    emails = ()

    # get members based on requested "group"
    self.stdout.write('''Groupmail from <'''+str(options['from'])+'''> to group: <'''+str(options['group'])+'''>''')

    if options['group'] == 'members':
      query = Member.objects.filter(Q(status=Member.ACT) | Q(status=Member.HON) | Q(status=Member.WBE))
#    elif options['group'] == 'board':
    elif options['group'] == 'test':
      query = Member.objects.filter(role__isnull=False)
    else:
      query = None

    # get email parts from raw source
    raw_message = email.message_from_string(str(options['message']))
    if raw_message.is_multipart():
      for payload in raw_message.get_payload():
        message = payload.get_payload()
    else:
        message = raw_message.get_payload()
    subject += str(raw_message['subject'])

    # send(forward) mail to people of selected group
    if query is not None:
      for m in query:
        emails += (
	  (
          	subject,
          	message,
        	options['from'],
          	[m.email,],
	  ),
	)
        self.stdout.write('Prepared message for <'+unicode(m)+'>')

    send_mass_mail(emails)
    self.stdout.write('Emails sent!')


