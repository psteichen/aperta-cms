from django.db.models import Model, EmailField, DateField, IntegerField, CharField, ForeignKey
from django.contrib.auth.models import User

class Member(Model):
  ACT = 0
  HON = 1
  WBE = 2
  STB = 3
  STATUSES = (
    (ACT, 'actif'),
    (HON, 'honoraire'),
    (WBE, 'aspirant (wouldbe)'),
    (STB, 'inactif (standby)'),
  )

  first_name    = CharField(max_length=100)
  last_name	= CharField(max_length=100)
  email		= EmailField()
  start_date    = DateField()
  end_date      = DateField(blank=True,null=True) 
  status      	= IntegerField(choices=STATUSES,default=ACT) 
  user		= ForeignKey(User,blank=True,null=True) 

  def __unicode__(self):
    return unicode(self.first_name) + ' ' + unicode.upper(self.last_name)

class Role(Model):
  title		= CharField(max_length=100)
  desc		= CharField(max_length=500,blank=True,null=True)
  member      	= ForeignKey(Member) 
  start_date    = DateField()
  end_date      = DateField(blank=True,null=True) 

  def __unicode__(self):
    return self.title + ' : ' + unicode(self.member)

  class Meta:
    unique_together = ( 'member', 'title', )

