# Application settings for setup app
# coding=utf-8

SETUP_TMPL_CONTENT = {
  'title'       	: u"Configuration système",
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
