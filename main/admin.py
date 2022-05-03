from django.contrib import admin

from main.models import BaseModel

for cls in BaseModel.__subclasses__():
    admin.site.register(cls)
