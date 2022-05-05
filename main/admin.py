from django.apps import apps
from django.contrib import admin

from contracts.models_products import ContractProduct


for cls in apps.get_models():
    try:
        admin.site.register(cls)
    except admin.sites.AlreadyRegistered:
        pass
