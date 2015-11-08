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
  title		= CharField(verbose_name=u'Titre',max_length=100)
  author	= CharField(verbose_name=u'Auteur',max_length=100)
  last_update	= DateField(verbose_name=u'Dernière mise à jour',)
  url		= URLField(verbose_name=u'URL',unique=True)
  elements	= ManyToManyField(Element)
  
  def __unicode__(self):
    return unicode(self.title) + ' - ' + unicode(self.url)

class Category(Model):
  title		= CharField(verbose_name=u'Catégorie',max_length=100)
  index		= ForeignKey(Page,verbose_name=u'Page d\'index')
  pages		= ManyToManyField(Page,related_name='+')

  def __unicode__(self):
    return unicode(self.title)


