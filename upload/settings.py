# Application settings for upload app
# coding=utf-8

ACTIONS = {
  'main' : (
    { 
      'label'         	: u'Importer des Membres', 
      'icon'     	: 'file',
      'grade'     	: 'danger',
      'url'           	: '/upload/members/', 
      'has_perms'	: 'cms.BOARD',
    },
    { 
      'label'         	: u'Importer le Calendrier', 
      'icon'     	: 'calendar',
      'grade'     	: 'danger',
      'url'           	: '/upload/calendar/', 
      'has_perms'	: 'cms.BOARD',
    },
  ),
}

UPLOAD_TMPL_CONTENT = {
  'title'       	: 'Membres',
  'template'  		: 'done.html',
  'actions'     	: ACTIONS['main'],
  'members': {
    'template'		: 'form.html',
    'title'     	: u'Importer des Membres',
    'desc'     		: u'''<p>L'import accepte uniquement des fichiers de type 'csv', utilisant le séparateur ";".</p><p>Veuillez trouver une exemple ci-dessous :</p>
<div class="well">
PRENOM ; NOM ; EMAIL ; ADRESSE ; TEL ; MOBILE</br>
Jean ; Dupont ; jean@dupont.lu ; 5, rue du Près L-1234 Mersch ; 36594812 ; 621894578<br/>
...
</div>
''',
    'submit'   		: u'Importer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'{} membre(s) importé(s).',
    },
  },
  'calendar': {
    'template'		: 'form.html',
    'title'     	: u'Importer le Calendrier des réunions',
    'desc'     		: u'''<p>L'import accepte uniquement des fichiers de type 'csv', utilisant le séparateur ";".</p><p>Veuillez trouver une exemple ci-dessous :</p>
<div class="well">
DATE ; TITRE ; TYPE</br>
29/09/2017 ; Réunion statutaire ; 0<br/>
15/07/2018 ; Fête de l'amitié du District ; 1</br/>
...
</div>
<p>Le TYPE définit le type de rencontre: "0" -> réunion statuaire ; "1" -> autre évènement non-statutaire.</p>
''',
    'submit'   		: u'Importer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'{} membre(s) importé(s).',
    },
  }
}
