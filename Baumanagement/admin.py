from django.contrib import admin

from .models import *  # Do not delete
from .models.abstract import BaseModel


for cls in BaseModel.__subclasses__():
    admin.site.register(cls)
