# Application settings for setup app
# coding=utf-8

SETUP_TMPL_CONTENT = {
  'title'       	: u"Configuration système",
  'template'  		: 'list.html',
  'init': {
    'template'		: 'form.html',
    'title'       	: u"Configuration initiale",
    'desc'     		: u'',
    'submit'  		: u'Soumettre',
    'done': {
      'title'       	: u"Prochaines étapes",
      'template'	: 'done.html',
      'message'     	: u'''
<a class="btn btn-lg btn-danger" href="/upload/members/" role="button"><i class="fa fa-users"></i>&nbsp;&nbsp;Importer la liste des membres</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a class="btn btn-lg btn-danger" href="/upload/calendar/" role="button"><i class="fa fa-calendar"></i>&nbsp;&nbsp;Importer le calendrier des réunions et évènements</a>
</div>'''
    },
  },
}
