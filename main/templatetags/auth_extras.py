from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='is_admin')
def is_admin(user):
    group = Group.objects.get_or_create(name='admins')[0]
    return group in user.groups.all()
