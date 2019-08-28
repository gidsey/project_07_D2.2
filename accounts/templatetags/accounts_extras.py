"""Custom template tags"""

from django import template

register = template.Library()

@register.filter('add_help_style')
def add_help_style(help_text):
    """Adds a class to the <ul> and <li> tags"""
    help_text = help_text.replace('<ul>', '<div>')
    help_text = help_text.replace('</ul>', '</div>')
    help_text = help_text.replace('<li>', '<div class="text-info p-1 mb-0">')
    help_text = help_text.replace('</li>', '</div>')
    return help_text
