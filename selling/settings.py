# Application settings for selling app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choisir l\'action sur les <strong>Members</strong>:',
    'has_perms'		: 'cms.BOARD',
    'actions'   : (
      {
        'label'         : 'Ajouter un Produit',
        'glyphicon'     : 'glyphicon-glass',
        'desc'          : 'Ceci ajoute un produit.', 
        'url'           : '/selling/add/',
   	'has_perms'	: 'cms.BOARD',
      },
      {
        'label'         : 'Liste des Produits',
        'glyphicon'     : 'glyphicon-glass',
        'desc'          : 'Tableau de tous les produits dans la base de donnée.',
        'url'           : '/selling/list/',
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
    'title'     	: ACTIONS[0]['actions'][0]['desc'],
    'desc'      	: ACTIONS[0]['actions'][0]['desc'],
    'first'             : u'début',
    'prev'              : u'précédent',
    'overview' : {
      'title'           : 'Overview',
    },
    'produit' : {
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
  'list': {
    'template'  	: 'list.html',
    'title'     	: 'List of Members',
    'desc'     		: '',
  },
  'order': {
    'template'		: 'form.html',
    'title'     	: u'Commander',
    'desc'      	: u'Acheter un Produit pour le revendre et récolter de l\'argent pour une bonne oeuvre.',
    'submit'            : u'soumettre',
    'done' : {
      'template'        : 'done.html',
      'title'           : u'Produit [%s] commandé!',
    },
  },
}
