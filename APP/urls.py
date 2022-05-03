from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import URLPattern, URLResolver
from django.urls import include, path
from django.views.static import serve

from Baumanagement.views import views_projects

urlpatterns = [
    path("", views_projects.objects_table, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('', include('Baumanagement.urls')),
    path('', include('first_run.urls')),
    path('', include('structure.urls')),
]


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, protected_serve, document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.my404'


def get_urls():
    result = []
    for each in list_urls(urlpatterns):
        url = ''.join(each)
        if 'accounts/' in url:
            continue
        if 'admin/' in url:
            continue
        if 'i18n/' in url:
            continue
        if 'media/' in url:
            continue
        result.append(f'/{url}'.replace('<int:id>', '1'))
    return result


def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)
