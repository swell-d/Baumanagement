from django import forms

from Baumanagement.models.models_messages import MyMessage
from Baumanagement.tables.tables_messages import MyMessageTable
from Baumanagement.views.views import myrender, generate_objects_table

baseClass = MyMessage
tableClass = MyMessageTable


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {}
    queryset = MyMessage.objects.filter(created_by=request.user)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)
