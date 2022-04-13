from django.contrib import admin

from Baumanagement.models.abstract import BaseModel
from Baumanagement.models.models_messages import MyMessage
from Baumanagement.models.models_settings import Settings

admin.site.register(MyMessage)
admin.site.register(Settings)

for cls in BaseModel.__subclasses__():
    admin.site.register(cls)
