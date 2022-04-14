from django import forms

from Baumanagement.models.models_messages import MyMessage
from Baumanagement.tables.tables import MyTable
from Baumanagement.views.views import myrender, generate_objects_table, get_base_context

baseClass = MyMessage


class TableClass(MyTable):
    class Meta(MyTable.Meta):
        model = baseClass
        fields = baseClass.table_fields

    def render_name(self, record, value):
        return value


class FormClass(forms.ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = get_base_context(request)
    queryset = MyMessage.objects.filter(created_by=request.user)
    generate_objects_table(request, context, baseClass, TableClass, FormClass, queryset)
    return myrender(request, context)
