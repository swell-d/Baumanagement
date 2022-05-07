import inspect
from datetime import datetime, timedelta

from django.db import IntegrityError
from django.forms import TextInput, forms
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig
from django_tables2.export import TableExport

from comments.models import Comment
from files.models import File
from main.comments import CommentFormClass, add_comment_to_object
from main.models import add_search_field, get_or_none
from main.upload_files import upload_files
from notifications.models import Notification
from projects.models import Project
from settings.models import Settings
from statistic.models import Visits, SearchQueries


class EmptyForm(forms.Form):
    base_fields = 'base',


def myrender(request, context):
    if request.POST \
            and not context.get('form', EmptyForm()).errors \
            and not context.get('productsform', EmptyForm()).errors:
        return redirect(request.path)

    export_format = request.GET.get("_export", None)
    if export_format and TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, context['table1'])
        return exporter.response("table.{}".format(export_format))

    context['projects'] = Project.objects.all()
    context['settings'] = Settings.objects.get_or_create(user=request.user)[0]

    template = 'tables/tables.html' if not request.GET else 'tables/maintable.html'
    return render(request, template, context)


def my404(request, exception):
    return HttpResponseNotFound(render(request, 'errors/404.html'))


def generate_objects_table(request, context, baseClass, tableClass, formClass, queryset=None):
    settings = context['settings']
    if 'created' in baseClass.table_fields:
        context['date_fields'] = True

    if not request.GET:
        context.setdefault('breadcrumbs_titel', baseClass._meta.verbose_name_plural)
        context.setdefault('breadcrumbs', [{'text': _("All")}])
        new_object_form(request, context, formClass)
        context['search_field'] = True
    # else:
    if queryset is None:
        queryset = baseClass.objects

    queryset = date_filter(request, queryset, baseClass, settings)
    queryset = label_filter(request, queryset)
    queryset = project_filter(request, baseClass, queryset, settings)

    if request.GET.get('sort'):
        settings.sort[baseClass.urls] = request.GET.get('sort')
        settings.save()

    queryset = baseClass.extra_fields(queryset)
    queryset = add_search_field(queryset, request)
    table1 = tableClass(queryset, order_by=settings.sort.get(baseClass.urls, '-created'), settings=settings)
    RequestConfig(request).configure(table1)
    context['table1'] = table1


def generate_object_table(request, context, baseClass, tableClass, formClass, queryset):
    settings = context['settings']
    if not request.GET:
        context.setdefault('breadcrumbs_titel', baseClass._meta.verbose_name)
        edit_object_form(request, context, formClass, queryset.first())

        comments = []
        for comment in [get_or_none(Comment, id=id) for id in queryset.first().comment_ids]:
            if comment:
                comments.append({
                    'object': comment,
                    'files': list(filter(None, [get_or_none(File, id=id) for id in comment.file_ids]))
                })
        context['tables'].append({'titel': _('Comments'), 'count': len(comments),
                                  'comments': comments, 'form': CommentFormClass(), 'files_form': []})
    # else:
    queryset = baseClass.extra_fields(queryset)
    table1 = tableClass(queryset, orderable=False, object_table=True, settings=settings)
    RequestConfig(request).configure(table1)
    context['table1'] = table1


def generate_next_objects_table(request, context, baseClass, tableClass, queryset, titel=None):
    settings = context['settings']
    queryset = baseClass.extra_fields(queryset)
    table = tableClass(queryset, order_by=settings.sort.get(baseClass.urls, '-created'), settings=settings,
                       orderable=2)  # hack. ordered, but without a links in header
    RequestConfig(request).configure(table)
    context['tables'].append({'table': table, 'titel': titel or baseClass._meta.verbose_name_plural,
                              'count': len(table.rows), 'link': f'{request.path}/{baseClass.urls}'})


def create_new_object_or_get_error(request, cls):
    if request.method != 'POST':
        return None
    formset = cls(request.POST, request.FILES)
    if formset.is_valid():
        try:
            new_object = formset.save(commit=False)
            new_object.save()
            formset.save_m2m()
            verbose_name = new_object.verbose_name()
            link = reverse(new_object.url_id, args=[new_object.id])
            Notification.message(
                request, f'{verbose_name} "<a href="{link}">{new_object.name}</a>" ' + _("created"), 'SUCCESS'
            )
            upload_files(request, new_object)
            add_comment_to_object(request, new_object)
            return None
        except IntegrityError:
            Notification.message(request, _("Object already exist"), 'ERROR')
    else:
        Notification.message(request, formset.errors, 'ERROR')
        return formset


def new_object_form(request, context, cls):
    error_form = create_new_object_or_get_error(request, cls)
    context['form'] = error_form or context.get('form') or cls()
    if 'FileModel' in str(inspect.getmro(cls.Meta.model)):
        context['files_form'] = []
    context['buttons'] = ['New']


def edit_object_form(request, context, cls, object):
    error_form = None
    if request.method == 'POST':
        if request.POST.get('mainObject'):
            formset = cls(request.POST, request.FILES, instance=object)
            if formset.is_valid():
                object = formset.save(commit=False)
                object.save()
                formset.save_m2m()
                verbose_name = object.verbose_name()
                link = reverse(object.url_id, args=[object.id])
                Notification.message(
                    request, f'{verbose_name} "<a href="{link}">{object.name}</a>" ' + _("changed"), 'SUCCESS'
                )
                upload_files(request, object)
            else:
                Notification.message(request, formset.errors, 'ERROR')
            error_form = formset
        elif request.POST.get('createCopy'):
            error_form = create_new_object_or_get_error(request, cls)
        elif request.POST.get('editProducts'):
            pass
    context['form'] = error_form or context.get('form') or cls(instance=object)
    if 'FileModel' in str(inspect.getmro(object.__class__)):
        context['files_form'] = object.files
    context['buttons'] = ['Edit']


def label_filter(request, queryset):
    label = request.GET.get('label')
    if label:
        if reverse('products') not in request.path:
            return queryset.filter(label__id=int(label))
        else:
            return queryset.filter(categories__id=int(label))
    return queryset


def date_filter(request, queryset, baseClass, settings):
    settings_df = settings.date_from
    if request.GET:
        date_from = request.GET.get('dateFrom')
        date_from = make_aware(datetime.strptime(date_from, "%Y-%m-%d")) if date_from else None
    else:
        date_from = settings_df
    if settings_df != date_from:
        settings.date_from = date_from
        settings.save()
    if date_from and 'created' in baseClass.table_fields:
        queryset = queryset.filter(created__gte=date_from)

    settings_dt = settings.date_to
    if request.GET:
        date_to = request.GET.get('dateTo')
        date_to = make_aware(datetime.strptime(date_to, "%Y-%m-%d")) if date_to else None
    else:
        date_to = settings_dt
    if settings_dt != date_to:
        settings.date_to = date_to
        settings.save()
    if date_to and 'created' in baseClass.table_fields:
        queryset = queryset.filter(created__lt=date_to + timedelta(days=1))

    return queryset


def project_filter(request, baseClass, queryset, settings):
    settings_ap_id = settings.active_project.id if settings.active_project else None
    if request.GET:
        project_id_str = request.GET.get('project')
        project_id = int(project_id_str) if project_id_str else None
    else:
        project_id = settings_ap_id
    if project_id != settings_ap_id:
        settings.active_project = Project.objects.get(id=project_id) if project_id else None
        settings.save()
    if project_id and baseClass.__name__ == 'Contract':
        queryset = queryset.filter(project_id=project_id)
    elif project_id and baseClass.__name__ in ['Bill', 'Payment']:
        queryset = queryset.filter(contract__project_id=project_id)
    return queryset


def get_base_context(request):
    visits = Visits.objects.get_or_create(page=request.path)[0]
    visits.count += 1
    visits.save()

    if request.GET.get("search"):
        searchquery = SearchQueries.objects.get_or_create(page=request.path, query=request.GET.get("search"))[0]
        searchquery.count += 1
        searchquery.save()

    return {'settings': Settings.objects.get_or_create(user=request.user)[0],
            'tables': []}


class ColorFieldWidget(TextInput):
    input_type = 'color'


def labels(cls):
    return {'objects': [each for each in cls.objects.order_by('path') if each.count],
            'urls': cls.urls}
