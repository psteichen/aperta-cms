# Application settings for members app
# coding=utf-8

ACTIONS = {
  'main' : (
    {
      'label'		: u'Ajouter',
      'icon'     	: 'plus',
      'url'           	: '/members/add/',
      'has_perms'	: 'cms.BOARD',
    },
  ),
  'modify' : (
    { 
      'label'         	: u'Ajouter un Rôle', 
      'icon'     	: 'plus',
      'url'           	: '/members/role/add/', 
      'has_perms'	: 'cms.BOARD',
    },
  ),
}

MEMBERS_TMPL_CONTENT = {
  'title'       	: 'Gestion des Membres',
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
    'actions'     	: ACTIONS['modify'],
    'first'             : u'début',
    'prev'              : u'retour',
    'overview' : {
      'title'           : u'Résumé',
    },
    'member' : {
      'title'           : 'Modify Member',
      'next'            : 'submit',
    },
    'role' : {
      'title'           : 'Modify Role',
      'next'            : 'submit',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Member [%s] modified!',
    },
  },
  'profile': {
    'template'  	: 'done.html',
    'title'     	: u'Profile utilisateur',
    'overview' : {
      'template'	: 'overview_member.html',
      'name'		: u'Nom',
      'username'	: u'Login',
      'email'		: u'E-mail',
      'role'		: u'Rôle',
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
