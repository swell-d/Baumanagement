from datetime import datetime, timedelta

from django.urls import reverse
from django.utils.timezone import make_aware

from projects.models import Project


def filter_objects_table(request, baseClass, queryset, settings):
    queryset = date_filter(request, queryset, baseClass, settings)
    queryset = label_filter(request, queryset)
    queryset = project_filter(request, baseClass, queryset, settings)
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


def label_filter(request, queryset):
    label = request.GET.get('label')
    if label:
        if reverse('products') not in request.path:
            return queryset.filter(label__id=int(label))
        else:
            return queryset.filter(categories__id=int(label))
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
