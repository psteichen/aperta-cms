# Application settings for web app
# coding=utf-8

ACTIONS = {
  'main' : (
    {
      'label'		: u'Nouvel Catégorie',
      'icon'     	: 'plus',
      'url'           	: '/web/category/add/',
      'has_perms'	: 'cms.BOARD',
    },
  ),
}

WEB_TMPL_CONTENT = {
  'title'       	: u'Site web',
  'template'  		: 'list.html',
  'actions'     	: ACTIONS['main'],
  'add': {
    'template'		: 'form.html',
    'title'     	: u'Ajouter un Membre',
    'desc'     		: u'Ajouter un nouveau membre, would-be ou autre.',
    'submit'   		: u'Ajouter',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Un nouveau Membre a été rajouté.',
      'message'     	: u'Détails : ',
    },
  },
  'modify': {
    'first'             : u'début',
    'prev'              : u'retour',
    'overview' : {
      'title'           : u'Résumé',
    },
    'member' : {
      'title'           : u'Modifier le Member',
      'next'            : 'enregistrer',
    },
    'mod_role' : {
      'title'           : u'Modifier le Rôle',
      'next'            : 'enregistrer',
    },
    'add_role' : {
      'title'           : u'Ajouter un rôle',
      'next'            : 'enregistrer',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Member [%s] modified!',
    },
  },
  'role' : {
    'add': {
      'template'	: 'form.html',
      'title'     	: u'Ajouter un Rôle',
      'desc'     	: '',
      'submit'   	: u'Ajouter',
      'done': {
        'template'	: 'done.html',
        'title'     	: u'Un nouveau Rôle a été rajouté.',
        'message'     	: u'Détails : ',
      },
    },
  },
}
