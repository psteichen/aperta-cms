# Application settings for selling app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choisir l\'action sur les <strong>Produits</strong>:',
    'has_perms'		: 'cms.BOARD',
    'actions'   : (
      {
        'label'         : 'Ajouter un Produit',
        'glyphicon'     : 'glyphicon-euro',
        'desc'          : 'Ceci ajoute un produit.', 
        'url'           : '/selling/add/',
   	'has_perms'	: 'cms.BOARD',
      },
      {
        'label'         : 'Liste des Produits',
        'glyphicon'     : 'glyphicon-euro',
        'desc'          : 'Tableau de tous les produits dans la base de donnée.',
        'url'           : '/selling/list_all/',
   	'has_perms'	: 'cms.BOARD',
      },
      {
        'label'         : 'Notification de nouveaux Produits',
        'glyphicon'     : 'glyphicon-euro',
        'desc'          : 'Envoie d\'un email d\'information sur les nouveaux produits',
        'url'           : '/selling/notify/',
   	'has_perms'	: 'cms.BOARD',
      },
    ),
  },
)

SELLING_TMPL_CONTENT = {
  'title'       : 'Achat/vente',
  'template'    : 'actions.html',
  'actions'     : ACTIONS,
  'add': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][0]['label'],
    'desc'      	: ACTIONS[0]['actions'][0]['desc'],
    'first'             : u'début',
    'prev'              : u'précédent',
    'overview' : {
      'title'           : 'Overview',
    },
    'product' : {
      'title'           : u'Créer un nouveau Produit',
      'next'            : 'suivant',
    },
    'packaging' : {
      'title'           : u'Définit le Packaging',
      'next'            : 'suivant',
    },
    'price' : {
      'title'           : u'Spécifier le Prix',
      'next'            : 'soumettre',
    },
    'done': {
      'template'	: 'done.html',
      'title'     	: 'Nouveau Produit ajouter.',
      'message'     	: u'Details ci-après: ',
    },
  },
  'notify': {
    'template'		: 'done.html',
    'title'     	: ACTIONS[0]['actions'][2]['label'],
    'desc'      	: ACTIONS[0]['actions'][2]['desc'],
    'message'     	: u'''
<pre>
Message d'information :
------------------------------
%(message)s
------------------------------

Destinataires :
------------------------------
%(recipients)s
------------------------------
</pre>
''',
    'email': {
      'template'	: 'selling_notify.txt',
      'subject'     	: '[51 eisleck] Vente de bienfaisance',
    },
  },
  'modify': {
    'title'     	: 'Modifier un Produit',
    'first'             : 'first',
    'prev'              : 'back',
    'overview' : {
      'title'           : 'Overview',
    },
    'produit' : {
      'title'           : 'Modifier le Produit',
      'next'            : 'suivant',
    },
    'packaging' : {
      'title'           : 'Modifier le Packaging',
      'next'            : 'suivant',
    },
    'price' : {
      'title'           : 'Modifier le Prix',
      'next'            : 'suivant',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : u'Produit [%s] modifié!',
    },
  },
  'list_all': {
    'template'  	: 'list.html',
    'title'     	: ACTIONS[0]['actions'][1]['label'],
    'desc'      	: ACTIONS[0]['actions'][1]['desc'],
  },
  'order': {
    'template'        	: 'order_form.html',
    'title'     	: u'Commander des Produits',
    'desc'      	: u'Acheter des Produits pour les revendre et récolter de l\'argent pour une bonne oeuvre.',
    'submit'            : 'soumettre',
    'done' : {
      'template'        : 'done.html',
      'title'           : u'Détail de votre Commande du %(date)s.',
      'email' : {
        'template'	: 'receipt.txt',
        'subject'	: '[51 eisleck] Commande du %(date)s.',
      },
    },
  },
}
