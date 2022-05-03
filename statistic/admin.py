from django.contrib import admin

from statistic.models import Visits, SearchQueries

admin.site.register(Visits)
admin.site.register(SearchQueries)
