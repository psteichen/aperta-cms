# Application settings for upload app
# coding=utf-8

ACTIONS = {
  'main' : (
    { 
      'label'         	: u'Importer des Membres', 
      'icon'     	: 'file',
      'grade'     	: 'warning',
      'url'           	: '/upload/members/', 
      'has_perms'	: 'cms.BOARD',
    },
    { 
      'label'         	: u'Importer le Calendrier', 
      'icon'     	: 'claendar',
      'grade'     	: 'info',
      'url'           	: '/upload/calendar/', 
      'has_perms'	: 'cms.BOARD',
    },
  ),
}

UPLOAD_TMPL_CONTENT = {
  'title'       	: 'Membres',
  'template'  		: 'done.html',
#  'actions'     	: ACTIONS['main'],
  'members': {
    'template'		: 'form.html',
    'title'     	: u'Importer des Membres',
    'desc'     		: u"L'import accepte uniquement des fichiers de type 'csv'.",
    'submit'   		: u'Importer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'{nb} nouveau(x) Membre(s) importé(s).',
      'message'     	: u'Détails : ',
    },
  },
}
