# Application settings for finance app
# coding=utf-8

ACTIONS = {
  'main' : (
    {
      'has_perms'     	: 'MEMBER',
      'heading'         : u'Bilan',
      'actions' : (
        {
          'label'     	: u'Comptes annuels',
          'desc'        : u"Les bilans financiers et les comptes des pertes et profits, tels qu'établient pour clôturer les périodes d'activitiées annuelles.",
          'icon'      	: 'balance-scale',
          'url'         : '/finance/balance/',
          'has_perms' 	: 'MEMBER',
        },
      ),
    },
    {
      'has_perms'     	: 'BOARD',
      'heading'         : u'Banque',
      'actions' : (
        {
          'label'     	: u'Extraits bancaires',
          'desc'        : u"Extraits et documents bancaires correspondant au compte de l'association.",
          'icon'      	: 'bank',
          'url'         : '/finance/bank/',
          'has_perms' 	: 'BOARD',
        },
      ),
    },
  ),
  'balance' : (
    {
      'label'         	: u'Télécharger les Comptes annuels',
      'icon'          	: 'balance-scale',
      'grade'     	: 'danger',
      'url'		: '/finance/upload/balance/',
      'has_perms'	: 'BOARD',
    },
  ),
  'bank' : (
    {
      'label'		: u'Nouvel Extrait',
      'icon'     	: 'bank',
      'grade'     	: 'danger',
      'url'           	: '/finance/bank/upload/bank/',
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
  'payment' : (
    {
      'label'		: u'Nouveau Payment',
      'icon'     	: 'euro',
      'grade'     	: 'danger',
      'url'           	: '/finance/payment/add/',
      'has_perms'	: 'BOARD',
    },
  ),
}

FINANCE_TMPL_CONTENT = {
  'title'       	: u'Trésorerie',
  'template'  		: 'actions.html',
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
  },
  'balance': {
    'template'          : 'list.html',
    'title'           	: u'Comptes annuels',
    'actions'         	: ACTIONS['balance'],
    'desc'              : u'',
  },
  'upload': {
    'template'          : 'form.html',
    'title'           	: u'Télécharger {name}',
    'desc'            	: u'',
    'submit'          	: u'Soumettre',
    'done': {
      'template'      	: 'done.html',
      'url'           	: '/finance/{type}/',
    },
  },
}
