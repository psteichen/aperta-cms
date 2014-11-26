from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, cl):
  try:
    return field.as_widget(attrs={'class' : cl,})
  except:
    return field

