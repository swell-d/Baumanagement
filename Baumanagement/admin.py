from django.contrib import admin

from .models import *
from .models.abstract import BaseModel
from .models.models_messages import MyMessage
from .models.models_settings import Settings

admin.site.register(MyMessage)
admin.site.register(Settings)

for cls in BaseModel.__subclasses__():
    admin.site.register(cls)
