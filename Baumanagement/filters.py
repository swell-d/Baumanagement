import re

import django_filters
from django.utils.html import format_html

from Baumanagement.models import Bill


def filter_form_prettify(filter_form):
    filter_form_text = str(filter_form)
    filter_form_text = re.sub('<label[\S\s]+?>([\S\s]+?):[\S\s]+?<input',
                              r'<input placeholder="\g<1>" onchange="this.form.submit()" ',
                              filter_form_text)
    filter_form_text = re.sub('type="number"', 'type="text"', filter_form_text)
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
