# Application settings for setup app
# coding=utf-8

ACTIONS = {
  'main' : (
    {
      'label'		: u'Extraits bancaires',
      'icon'     	: 'bank',
      'grade'     	: 'info',
      'url'           	: '/finance/bank/',
      'has_perms'	: 'BOARD',
    },
  ),
  'invoice' : (
    {
      'label'		: u'Nouvelle Facture',
      'icon'     	: 'euro',
      'grade'     	: 'danger',
      'url'           	: '/finance/invoice/add/',
      'has_perms'	: 'BOARD',
    },
  ),
}

SETUP_TMPL_CONTENT = {
  'title'       	: u"Configuration de l'environnement",
  'template'  		: 'list.html',
#  'actions'     	: ACTIONS['main'],
  'init': {
    'template'		: 'form.html',
    'title'       	: u"Configuration initiale",
    'desc'     		: u'',
    'submit'  		: u'Soumettre',
    'done': {
        'template'	: 'done.html',
        'url'     	: '/',
    },
  },
}
