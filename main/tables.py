import re
import urllib.parse

import django_tables2 as tables
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

modal = '#ModalForm" data-bs-toggle="modal" data-bs-target="#ModalForm'
default_timezone = timezone.get_default_timezone()


def delete_none_values(value):
    return str(value) if value is not None else ''


class MyTable(tables.Table):
    id = tables.Column(visible=False)
    name = tables.Column(attrs={'td': {'class': 'fw-bold table-secondary'}}, footer="")

    def __init__(self, *args, **kwargs):
        self.object_table = kwargs.pop('object_table', False)
        self.settings = kwargs.pop('settings', None)
        super().__init__(*args, **kwargs)

    class Meta:
        empty_text = _("No results found")
        template_name = r"custom/django_tables2_custom.html"
        attrs = {'class': 'table table-hover', "thead": {"class": "table-secondary"}}  # table-sm
        row_attrs = {"class": lambda record: "text-muted" if not record.open else ""}

    def render_id(self, record, value):
        return base_render(self, record, value)

    def render_created(self, record, value):
        dtf = self.settings.datetime_format if self.settings else "%d.%m.%Y %H:%M"
        df = self.settings.date_format if self.settings else "%d.%m.%y"
        text = f'''
<a href="{modal if self.object_table else get_link(record)}">
    {record.created.astimezone(default_timezone).strftime(df)} 
</a>
<div class="mytooltip">
    &#9432;
    <span class="mytooltiptext small">
        <strong>{_("Created")}</strong>:<br> 
        {record.created.astimezone(default_timezone).strftime(dtf)}<br>
        {_("by")} <em>{record.author}</em><br> 
        
'''
        if record.created != record.updated:
            text += f'''
        <br>
        <strong>{_("Updated")}</strong>:<br>
        {record.updated.astimezone(default_timezone).strftime(dtf)}<br>
        {_("by")} <em>{record.updated_by}</em>
'''
        text += f'''
    </span>
</div>
'''
        return format_html(text)

    def render_author__settings__img(self, record, value):
        return format_html(f'''<img src={value.url} width=24 height=24/>''')

    def render_name(self, record, value):
        return base_render(self, record, value)

    def render_code(self, record, value):
        return base_render(self, record, value)

    def render_date(self, record, value):
        return date_render(self, record, value)

    def render_tag(self, record, value):
        return base_render(self, record, value)

    def render_company(self, record, value):
        link = reverse('company_id', args=[record.company.id])
        return format_html(f'<a href="{link}">{value}🔗</a>')

    def render_project(self, record, value):
        link = reverse('project_id', args=[record.project.id])
        return format_html(f'<a href="{link}">{value}🔗</a>')

    def render_contract(self, record, value):
        link = reverse('contract_id', args=[record.contract.id])
        return format_html(f'<a href="{link}">{value}🔗</a>')

    def render_currency(self, record, value):
        return base_render(self, record, value)

    def render_amount_netto(self, record, value):
        return format_amount(value, get_link(record), record.currency.symbol)

    def render_amount_netto_positiv(self, record, value):
        return self.render_amount_netto(record, value)

    def render_vat(self, record, value):
        return base_render(self, record, value)

    def render_amount_brutto(self, record, value):
        return format_amount(value, get_link(record), record.currency.symbol)

    def render_amount_brutto_positiv(self, record, value):
        return self.render_amount_brutto(record, value)

    def render_phone(self, record, value):
        return format_html(f'<a href="tel:{re.sub("[^0-9+]", "", value)}">{value}</a>')

    def render_address(self, record, value):
        return get_google_maps_link(record)

    def render_path(self, record, value):
        return format_html(f'<a href="{modal if self.object_table else get_link(record)}" class="badge" '
                           f'style="background-color:{record.color};">{value}</a>')

    def render_label(self, record, value):
        return format_html(
            " ".join([f'<a href="{reverse(record.url_id, args=[record.id])}" class="badge" style="background-color: '
                      f'{label.color};">{label}</a>' for label in value.all()]))

    def as_values(self, exclude_columns=None):
        if exclude_columns is None:
            exclude_columns = ()

        columns = [
            column
            for column in self.columns.iterall()
            if not (column.column.exclude_from_export or column.name in exclude_columns)
        ]

        yield [force_str(column.header, strings_only=True) for column in columns]

        for row in self.rows:
            yield [re.sub('<[^<]+?>', '', delete_none_values(force_str(row.get_cell_value(column.name),
                                                                       strings_only=True))) for column in columns]


class SummingColumnInt(tables.Column):
    def render_footer(self, bound_column, table):
        val = sum(bound_column.accessor.resolve(cell) or 0 for cell in table.data if cell.open)
        return format_html(
            f'''<span class="{'text-danger' if val < 0 else ''}">{val: .0f}</span>''' if val != 0 else '—')


class SummingColumn2F(tables.Column):
    def render_footer(self, bound_column, table):
        val = sum(
            float(bound_column.accessor.resolve(cell) or 0) / cell.currency.rate for cell in table.data if cell.open)
        return format_html(
            f'''<span class="{'text-danger' if val < 0 else ''}">{val: .2f} €</span>''' if val != 0 else '—')


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

    # def order_files(self, queryset, is_descending):
    #     queryset = queryset.annotate(countfiles=Length('file_ids')).order_by(
    #         ("-" if is_descending else "") + "countfiles")
    #     return (queryset, True)


def get_google_maps_link(record):
    link = urllib.parse.quote_plus(record.address + " " + record.city + " " + record.land)
    text = f'{record.address}, {record.city}'
    text += f', {record.land}' if record.land != 'Deutschland' else ''
    return format_html(f'<a href="https://www.google.de/maps/search/{link}" target="_blank">{text}</a>')


def get_link(record):
    return reverse(record.url_id, args=[record.id])


def format_amount(value, link, symbol, arrow=False):
    return format_html(
        f'''<a href="{link}"{' class="text-danger"' if value < 0 else ''}>{value:.2f}&nbsp;{symbol}{'&nbsp;&#8694;' if arrow else ''}</a> ️''')


def base_render(tbl, record, value):
    return format_html(f'<a href="{modal if tbl.object_table else get_link(record)}">{value}</a>')


def date_render(tbl, record, value):
    return format_html(f'<a href="{modal if tbl.object_table else get_link(record)}">'
                       f'{value.strftime("%d.%m.%Y") if value else "—"}</a>')
