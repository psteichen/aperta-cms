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

from cms.functions import notify_by_email
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
    group = str(options.get('group'))
    subject = settings.EMAILS['tag'] + ' [' + str.upper(group) + '] '
    emails = ()

    # get raw email message
    message = email.message_from_string(options.get('message').read())
    mail = mailparser.parse_from_string(options.get('message').read())

    # get email parts from raw source
#    body = message.get_body()
#    attachments = message.iter_attchments()
#    body = ''
#    attachments = []
#    if message.is_multipart():
#      for part in message.walk():
#        if part.get_content_maintype() == 'multipart':
#          if part.get('Content-Disposition') is None:
#            filename = part.get_filename()
#            payload = part.get_payload(decode=True)
#            attachments.append({'name':filename,'content':payload})
#          else:
#            body += part.get_payload()
#    else:
#      body = message.part.get_payload()

    sender = str(message['from'])
    dest = str(message['to'])
    message.replace_header('Reply-To', group+'@'+settings.EMAILS['domain'])
    subject += str(message['subject'])
    message.replace_header('Subject', subject)

#    self.stdout.write(self.style.NOTICE('''Groupmail from <'''+str(sender)+'''> to group: <'''+str(group)+'''>'''))

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

#        notify_by_email(
#		sender,
#		m.email,
#		subject,
#		body,
#		False,
#		attachments,
#		False
#        )
#        emails += (
#	  (
#          	subject,
#          	msg.as_string(),
#        	sender,
#          	[m.email,],
#	  ),
#	)
#        self.stdout.write(self.style.NOTICE('Prepared message for <'+str(m)+'>'))
#        self.stdout.write(self.style.NOTICE('Sending message for <'+str(m)+'>'))

#    send_mass_mail(emails)
    server.quit()
#    self.stdout.write(self.style.SUCCESS('Emails sent!'))


