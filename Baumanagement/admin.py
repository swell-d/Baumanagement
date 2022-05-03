from django.contrib import admin

from .models import *  # Do not delete
from main.models import BaseModel

for cls in BaseModel.__subclasses__():
    admin.site.register(cls)
