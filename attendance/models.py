# coding=utf-8

from django.db.models import Model, ForeignKey, BooleanField, DateTimeField

from meetings.models import Meeting
from members.models import Member
from events.models import Event

class Meeting_Attendance(Model):
  meeting	= ForeignKey(Meeting)
  member	= ForeignKey(Member)
  timestamp	= DateTimeField()
  present	= BooleanField()
  
  def __unicode__(self):
    present = ''
    if self.present == True:
      present = 'YES'
    elif self.present == False:
      present = 'NO'
    return unicode(self.member) + ' / ' + unicode(self.meeting) + ' (' + unicode(self.timestamp) +') - ' + present


  class Meta:
    unique_together = ( 'member', 'meeting', )

class Event_Attendance(Model):
  event		= ForeignKey(Event)
  member	= ForeignKey(Member)
  timestamp	= DateTimeField()
  present	= BooleanField()
  
  def __unicode__(self):
    present = ''
    if self.present == True:
      present = 'YES'
    elif self.present == False:
      present = 'NO'
    return unicode(self.member) + ' / ' + unicode(self.event) + ' (' + unicode(self.timestamp) +') - ' + present


  class Meta:
    unique_together = ( 'member', 'event', )
