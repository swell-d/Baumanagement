from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect


def first_run(request):
    if User.objects.exclude(username='system'):
        return redirect('/')

    group = Group.objects.get_or_create(name='admins')[0]
    # User.objects.create_superuser(username, email, password)

    return HttpResponse('first run')
