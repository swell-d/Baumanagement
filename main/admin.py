from django.apps import apps
from django.contrib import admin

models = apps.get_models()

for cls in models:
    try:
        admin.site.register(cls)
    except admin.sites.AlreadyRegistered:
        pass
