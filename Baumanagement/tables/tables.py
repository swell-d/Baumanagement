import urllib.parse

import django_tables2 as tables
from django.db.models.functions import Length
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class TableDesign:
    empty_text = _("No results found")
    template_name = "django_tables2_custom.html"
    attrs = {'class': 'table table-hover'}
    row_attrs = {"class": lambda record: "text-muted" if not record.open else ""}


class SummingColumnInt(tables.Column):
    def render_footer(self, bound_column, table):
        val = sum(bound_column.accessor.resolve(row) or 0 for row in table.data if row.open)
        return f'{val: .0f}' if val != 0 else ''


class SummingColumn2F(tables.Column):
    def render_footer(self, bound_column, table):
        val = sum(bound_column.accessor.resolve(row) or 0 for row in table.data if row.open)
        return f'{val: .2f}' if val != 0 else ''


class Files:
    def render_files(self, record):
        text = ''.join([f'<a href="{each.file.url}" target="_blank">{str(each)[str(each).rfind(".") + 1:].upper()}</a>'
                        for each in record.files[:1]])
        if len(record.files) > 1:
            text = f'''
<div class="dropdown">
    {text}
    <a class="btn btn-outline-secondary btn-sm ms-2" href="#" role="button" 
    id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
        +{len(record.files) - 1}
    </a>
    <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
        {''.join([f'<li><a class="dropdown-item" href="{each.file.url}" target="_blank">{str(each)}</a></li>'
                  for each in record.files])}
    </ul>
</div>'''
        return format_html(text or '—')

    def order_files(self, queryset, is_descending):
        queryset = queryset.annotate(countfiles=Length('file_ids')).order_by(
            ("-" if is_descending else "") + "countfiles")
        return (queryset, True)


def get_google_maps_link(record):
    link = urllib.parse.quote_plus(record.address + " " + record.city + " " + record.land)
    text = f'{record.address}, {record.city}'
    text += f', {record.land}' if record.land != 'Deutschland' else ''
    return format_html(f'<a href="https://www.google.de/maps/search/{link}" target="_blank">{text}</a>')
