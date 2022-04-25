from django.contrib import admin

from .models import *  # Do not delete
from .models.abstract import BaseModel
from .models.models_messages import MyMessage
from .models.models_settings import Settings, Visits, SearchQueries

admin.site.register(MyMessage)
admin.site.register(Settings)
admin.site.register(Visits)
admin.site.register(SearchQueries)

for cls in BaseModel.__subclasses__():
    admin.site.register(cls)
