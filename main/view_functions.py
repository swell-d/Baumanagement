from settings.models import Settings
from statistic.models import Visits, SearchQueries


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


def labels(cls):
    return {'objects': [each for each in cls.objects.order_by('path') if each.count],
            'urls': cls.urls}
