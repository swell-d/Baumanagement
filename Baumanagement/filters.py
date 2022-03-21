import django_filters
from django.utils.html import format_html

from Baumanagement.models import Bill

filter_form_replaces = [
    ('<input', '<input onchange="this.form.submit()"'),
    ('<select', '<select onchange="this.form.submit()"'),
    ('type="number"', 'type="text"')
]


def filter_form_prettify(filter_form):
    filter_form_text = str(filter_form)
    for each in filter_form_replaces:
        filter_form_text = filter_form_text.replace(each[0], each[1])
    return format_html(filter_form_text)


class BillFilter(django_filters.FilterSet):
    class Meta:
        model = Bill
        fields = {}
        fields['name'] = ['contains']
        fields['contract__name'] = ['contains']
        fields['amount'] = ['contains']

    def __init__(self, *args, **kwargs):
        super(BillFilter, self).__init__(*args, **kwargs)
        self.filters['contract__name__contains'].label = 'Auftrag enthält:'
