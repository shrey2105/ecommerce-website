import ast

def literal_eval(value):
    return ast.literal_eval(value)

from django import template
register = template.Library()
register.filter('literal_eval', literal_eval)