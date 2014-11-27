# Application settings for attendance app
# coding=utf-8

ATTENDANCE_TMPL_CONTENT = {
  'template'	: 'done.html',
  'too_late' 	: u'Désolé il est <strong>trop tard</strong> pour s\'inscrire/désister!',
  'yes'  	: u''''<p>%(name)s, par la présente ta <strong>participation</strong> est <strong>confirmé(e)</strong></p>!
<a href="/meetings/wouldbe/%(meeting_num)s/%(attendance_hash)s/" class="btn btn-info">Inviter un "WouldBe" (?)</a>
''',
  'no'  	: u'%(name)s, merci de nous avoir notifier ton désistement, tu sera <strong>excusé(e)</strong>!',
  'event': {
    'title'	: u'Participation à l\'événement "%(event)s"',
    'email' : {
      'yes'	: u'''
Par la présente ta participation à l\'événement "%(event)s" est confirmé(e)!''',
      'no'  	: u'''
Merci de nous avoir notifier ton désistement, pour l\'événement "%(event)s". 

Tu sera excusé(e).''',
    },
  },
  'meeting': {
    'title'      : u'Participation à la %(meeting)s',
    'email' : {
      'yes'	: u'''
Par la présente ta participation à la %(meeting)s est confirmé(e)!''',
      'no'  	: u'''
Merci de nous avoir notifier ton désistement, pour la %(meeting)s. 

Tu sera excusé(e).''',
    },
  },
}

