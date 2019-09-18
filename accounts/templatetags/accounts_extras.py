"""Custom template tags"""

from django import template

register = template.Library()


@register.simple_tag
def show_panel(collapse):
    if collapse:
        return 'collapse.show'
    else:
        return 'collapse'


@register.filter('add_help_style')
def add_help_style(help_text):
    """Adds a class to the <ul> and <li> tags"""
    help_text = help_text.replace('<ul>', '<div>')
    help_text = help_text.replace('</ul>', '<br>')
    help_text = help_text.replace('<li>', '<div class="alert alert-info">')
    help_text = help_text.replace('</li>', '</div>')
    return help_text

