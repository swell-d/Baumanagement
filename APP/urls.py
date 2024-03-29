import glob
from os.path import join
from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import URLPattern, URLResolver
from django.urls import include, path
from django.views.static import serve

import projects.views

urlpatterns = [
    path('', projects.views.objects_table, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

for each in glob.glob(join(settings.BASE_DIR / '*', "urls.py")):
    if 'APP' in each:
        continue
    app = Path(each).resolve().parent.name
    urlpatterns += [path('', include(f'{app}.urls'))]


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, protected_serve, document_root=settings.MEDIA_ROOT)

handler404 = 'main.errors.my404'


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
