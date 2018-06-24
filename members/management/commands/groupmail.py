import re
import sys
import argparse
from optparse import make_option
import mailparser
import smtplib, email

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail, EmailMessage
from django.db.models import Q
from django.conf import settings

from members.models import Member

class Command(BaseCommand):
  def add_arguments(self, parser):

    # Positional arguments
    parser.add_argument('message', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    # Named (optional) arguments
    parser.add_argument(
      '--group', 
      dest='group',
      help='GROUP to send message to', 
      metavar='GROUP',
    )

  def handle(self, *args, **options):
    query = None
    group = options.get('group')
    subject = settings.EMAILS['tag'] + ' [' + str.upper(str(options['group'])) + '] '
    emails = ()

    # get raw email message
    message = email.message_from_string(options.get('message').read())
#    mail = mailparser.parse_from_string(options.get('message').read())

    # get email parts from raw source
#    body = None
#    if raw_message.is_multipart():
#      for payload in raw_message.get_payload():
#        body = payload.get_payload()
#        break
#    else:
#      body = raw_message.get_payload()

#    email_header = raw_message.walk().next()
#    sender = str(email_header['From'])
#    subject += str(email_header['Subject'])
    sender = message['From']
    message.replace_header("Subject", subject + str(message["Subject"]))

    self.stdout.write(self.style.NOTICE('''Groupmail from <'''+str(sender)+'''> to group: <'''+str(group)+'''>'''))

    # get members based on requested "group"
    if group == 'members':
      query = Member.objects.filter(Q(status=Member.ACT) | Q(status=Member.HON) | Q(status=Member.WBE))
    elif group == 'board':
      query = Member.objects.filter(role__isnull=False)
    else:
      query = None

    # send(forward) mail to people of selected group
    server = smtplib.SMTP('localhost')
    if query is not None:
      for m in query:
        message.replace_header("To", m.email)
        server.sendmail(sender, m.email, message.as_string())
#        emails += (
#	  (
#          	subject,
#          	message.as_string(),
#        	sender,
#          	[m.email,],
#	  ),
#	)
#        self.stdout.write(self.style.NOTICE('Prepared message for <'+str(m)+'>'))
        self.stdout.write(self.style.NOTICE('Sending message for <'+str(m)+'>'))

#    send_mass_mail(emails)
    server.quit()
    self.stdout.write(self.style.SUCCESS('Emails sent!'))


