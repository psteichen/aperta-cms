# Application settings for finance app
# coding=utf-8

ACTIONS = {
  'main' : (
    {
      'label'		: u'Extraits bancaires',
      'icon'     	: 'bank',
      'url'           	: '/finance/bank/',
      'has_perms'	: 'cms.BOARD',
    },
  ),
  'invoice' : (
    {
      'label'		: u'Nouvelle Facture',
      'icon'     	: 'euro',
      'url'           	: '/finance/invoice/add/',
      'has_perms'	: 'cms.BOARD',
    },
  ),
  'payment' : (
    {
      'label'		: u'Nouveau Payment',
      'icon'     	: 'euro',
      'url'           	: '/finance/payment/add/',
      'has_perms'	: 'cms.BOARD',
    },
  ),
  'bank' : (
    {
      'label'		: u'Nouvel Extrait',
      'icon'     	: 'file',
      'grade'     	: 'warning',
      'url'           	: '/finance/bank/upload/',
      'has_perms'	: 'cms.BOARD',
    },
  ),
}

FINANCE_TMPL_CONTENT = {
  'title'       	: u'Trésorerie',
  'template'  		: 'list.html',
  'actions'     	: ACTIONS['main'],
  'invoice': {
    'template'		: 'list.html',
    'title'     	: u'Factures',
    'actions'     	: ACTIONS['invoice'],
    'desc'     		: u'',
    'add': {
      'template'	: 'form.html',
      'title'     	: u'Nouvelle Facture',
      'desc'   		: u'',
    },
  },
  'payment': {
    'template'		: 'list.html',
    'title'     	: u'Payements',
    'actions'     	: ACTIONS['payment'],
    'desc'     		: u'',
    'add': {
      'template'	: 'form.html',
      'title'     	: u'Nouveau Payement',
      'desc'   		: u'',
    },
  },
  'bank': {
    'template'		: 'list.html',
    'title'     	: u'Extraits bancaires',
    'actions'     	: ACTIONS['bank'],
    'desc'     		: u'',
    'upload': {
      'template'	: 'form.html',
      'title'     	: u'Nouvel Extrait',
      'desc'   		: u'',
      'submit'  	: u'Soumettre',
      'done': {
        'template'	: 'done.html',
        'url'     	: '/finance/bank/',
      },
    },
  },
}
