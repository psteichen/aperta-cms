# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, ManyToManyField, IntegerField, URLField

class Element(Model):
  TXT = 0
  LNK = 1
  IMG = 2
  GAL = 3
  VID = 4
  HTM = 5
  TYPES = (
    (TXT, 'Text'),
    (LNK, 'Link'),
    (IMG, 'Image'),
    (GAL, 'Picture gallery'),
    (VID, 'Video'),
    (HTM, 'HTML content'),
  )

  type		= IntegerField()
  content	= CharField(max_length=500)

  def __unicode__(self):
    return unicode(self.type) + '[ ' + unicode(self.content) + ' ]'

class Page(Model):
  title		= CharField(max_length=100)
  author	= CharField(max_length=100)
  last_update	= DateField()
  url		= URLField(unique=True)
  elements	= ManyToManyField(Element)
  
  def __unicode__(self):
    return unicode(self.title) + ' - ' + unicode(self.url)

class Category(Model):
  title		= CharField(max_length=100)
  index		= ForeignKey(Page)
  pages		= ManyToManyField(Page,related_name='+')

  def __unicode__(self):
    return unicode(self.title)


