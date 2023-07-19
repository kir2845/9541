from django import template

register = template.Library()

@register.filter()
def censor(value):
   stop_list = ['погода', 'бал', 'год']
   post_list = value.split()
   post_clean = []
   for clean in post_list:
      if clean in stop_list:
         clean = clean[0]+'*'*(len(clean)-1)
         post_clean.append(clean)
      else:
         post_clean.append(clean)

   return f'{" ".join(post_clean)}'