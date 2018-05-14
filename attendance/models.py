# coding=utf-8

from django.db.models import Model, ForeignKey, BooleanField, DateTimeField, CharField

from meetings.models import Meeting
from members.models import Member
from events.models import Event

class Meeting_Attendance(Model):
  meeting	= ForeignKey(Meeting)
  member	= ForeignKey(Member)
  timestamp	= DateTimeField()
  present	= BooleanField(default=False)
  
  def __str__(self):
    present = ''
    if self.present == True:
      present = 'YES'
    elif self.present == False:
      present = 'NO'
    return str(self.member) + ' / ' + str(self.meeting) + ' (' + str(self.timestamp) +') - ' + present

  class Meta:
    unique_together = ( 'member', 'meeting', )

class MtoM(Model):
  meeting	= ForeignKey(Meeting)
  member	= ForeignKey(Member)
  yes_hash   	= CharField(max_length=250)
  no_hash   	= CharField(max_length=250)

  def __str__(self):
    return str(self.meeting) + ' - ' + str(self.member)


class Event_Attendance(Model):
  event		= ForeignKey(Event)
  member	= ForeignKey(Member)
  timestamp	= DateTimeField()
  present	= BooleanField(default=False)
  
  def __str__(self):
    present = ''
    if self.present == True:
      present = 'YES'
    elif self.present == False:
      present = 'NO'
    return str(self.member) + ' / ' + str(self.event) + ' (' + str(self.timestamp) +') - ' + present

  class Meta:
    unique_together = ( 'member', 'event', )

class EtoM(Model):
  event		= ForeignKey(Event)
  member	= ForeignKey(Member)
  yes_hash   	= CharField(max_length=250)
  no_hash   	= CharField(max_length=250)

  def __str__(self):
    return str(self.event) + ' - ' + str(self.member)



