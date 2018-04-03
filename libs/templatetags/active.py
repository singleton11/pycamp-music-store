from django import template
from django.core.urlresolvers import resolve

register = template.Library()


@register.filter(name="activate", is_safe=True)
def activate_if_active(request, urlname):
    """Highlight menu html element with active class

    taken from here:
    http://stackoverflow.com/questions/340888/navigation-in-django
    probably a better idea is to use multiple patterns solution
    see at the end of the SO answer above url
    """
    if resolve(request.get_full_path()).url_name == urlname:
        return "active"
    return ''
