from django.contrib import admin

from Baumanagement.models.models import Company, CompanyRole, Project, Contract, Payment, Bill, File


class FileInline(admin.TabularInline):
    model = File
    extra = 1


class FileAdmin(admin.ModelAdmin):
    inlines = [FileInline, ]


admin.site.register(CompanyRole)
admin.site.register(Company, FileAdmin)
admin.site.register(Project, FileAdmin)
admin.site.register(Contract, FileAdmin)
admin.site.register(Bill, FileAdmin)
admin.site.register(Payment, FileAdmin)
admin.site.register(File)
