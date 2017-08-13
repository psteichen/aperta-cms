# Application settings for members app
# coding=utf-8

ACTIONS = {
  'main' : (
    {
      'label'		: u'Nouveau Membre',
      'icon'     	: 'plus',
      'grade'     	: 'danger',
      'url'           	: '/members/add/',
      'has_perms'	: 'cms.BOARD',
    },
    {
      'label'		: u'Importer des Membres',
      'icon'     	: 'upload',
      'grade'     	: 'danger',
      'url'           	: '/upload/members/',
      'has_perms'	: 'cms.BOARD',
    },
    {
      'label'         : u'Gestion des Rôles',
      'icon'          : 'graduation-cap',
      'grade'         : 'warning',
      'url'           : '/members/roles/',
      'has_perms'     : 'cms.BOARD',
    },
  ),
  'roles' : (
    {
      'label'         : u'Nouveau Rôle',
      'icon'          : 'plus',
      'grade'         : 'warning',
      'url'                   : '/members/roles/add/',
      'has_perms'     : 'cms.BOARD',
    },
    {
      'label'         : u'Nouveau Rôle-Type',
      'icon'          : 'cog',
      'grade'         : 'warning',
      'url'                   : '/members/roles/type/',
      'has_perms'     : 'cms.BOARD',
    },
  ),
  'profile' : (
    {
      'label'		: u'Modifier',
      'icon'     	: 'pencil',
      'grade'     	: 'info',
      'url'           	: '/members/profile/modify/{}/',
      'has_perms'	: 'cms.MEMBER',
    },
    {
      'label'		: u'Back-office',
      'icon'     	: 'king',
      'grade'     	: 'warning',
      'url'           	: '/admin/',
      'has_perms'	: 'superuser',
    },
  ),
}

MEMBERS_TMPL_CONTENT = {
  'title'       	: 'Membres',
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
    'template'                : 'form.html',
    'title'           : u'Modifier le Membre',
    'desc'                    : u"Modifier les détails (adresse, tél, email, photo, etc.) d'un.",
    'submit'                  : u'Enregistrer',
    'done': {
      'template'      : 'done.html',
      'title'           : u'Le membre [{}] a été modifié!',
    },
  },
  'profile': {
    'template'  	: 'done.html',
    'actions'     	: ACTIONS['profile'],
    'title'     	: u'Profile utilisateur',
    'overview' : {
      'template'	: 'overview_member.html',
      'photo'		: u'Photo',
      'name'		: u'Nom',
      'address'		: u'Address',
      'username'	: u'Login',
      'mobile'		: u'Tél. mobile',
      'email'		: u'E-mail',
      'phone'		: u'Tél. fixe',
      'role'		: u'Rôle',
    },
    'modify': {
      'template'	: 'form.html',
      'title'     	: u'Modifier votre profile membre',
      'desc'     	: u'Modifier votre profile membre',
      'submit'   	: u'Modifier',
      'done': {
        'template'	: 'done.html',
        'title'     	: u'Votre profile membre a été ajusté.',
        'message'     	: u'Détails : ',
      },
    },
  },
  'roles' : {
    'title'           	: u'Rôles',
    'template'        	: 'list.html',
    'actions'         	: ACTIONS['roles'],
    'add': {
      'template'	: 'form.html',
      'title'         	: u'Nouveau Rôle',
      'desc'     	: '',
      'submit'        	: u'Enregistrer',
      'done': {
        'template'	: 'done.html',
        'title'       : u'Le rôle a été créé.',
      },
    },
    'modify': {
      'template'      : 'form.html',
      'title'         : u'Modifié un Rôle',
      'desc'          : '',
      'submit'        : u'Enregistrer',
      'done': {
        'template'    : 'done.html',
        'title'       : u'Le rôle a été modifié.',
      },
    },
    'type': {
      'template'      : 'form.html',
      'title'         : u'Nouveau Rôle-Type',
      'desc'          : '',
      'submit'        : u'Enregistrer',
      'done': {
        'template'    : 'done.html',
        'title'       : u'Le rôle-type a été créé.',
      },
    },
  },
}
