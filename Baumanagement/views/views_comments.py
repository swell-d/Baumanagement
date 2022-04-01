from django.forms import ModelForm
from django.shortcuts import redirect

from Baumanagement.models.models_comments import Comment
from Baumanagement.tables.tables_comments import CommentTable
from Baumanagement.views.views import myrender, generate_object_table, generate_objects_table

baseClass = Comment
tableClass = CommentTable


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    if request.method == 'POST' and request.POST.get('newCommentNextURL'):
        return redirect(request.POST.get('newCommentNextURL'))
    return myrender(request, context)


def object_table(request, id):
    context = {'tables': []}
    queryset = baseClass.objects.filter(id=id)
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)
