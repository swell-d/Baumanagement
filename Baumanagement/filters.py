import re

import django_filters
from django.utils.html import format_html

from Baumanagement.models import Bill, Company, Project, Contract, Payment


def filter_form_prettify(filter_form):
    filter_form_text = str(filter_form)
    filter_form_text = re.sub('<label[\S\s]+?>([\S\s]+?):[\S\s]+?<input',
                              r'<input placeholder="\g<1>" onchange="this.form.submit()" ',  # onchange oninput
                              filter_form_text)
    filter_form_text = re.sub('<select', '<select onchange="this.form.submit()"', filter_form_text)
    filter_form_text = re.sub('type="number"', 'type="text"', filter_form_text)

    filter_form_text = re.sub('<\/?tr>', '', filter_form_text)
    filter_form_text = re.sub('<\/?th>', '', filter_form_text)
    filter_form_text = re.sub('<\/?td>', '', filter_form_text)
    filter_form_text = re.sub('step="any"', '', filter_form_text)

    return format_html(filter_form_text)


class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {}
        fields['name'] = ['contains']


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = {}
        fields['name'] = ['contains']
        fields['open'] = ['exact']


class ContractFilter(django_filters.FilterSet):
    class Meta:
        model = Contract
        fields = {}
        fields['name'] = ['contains']


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {}
        fields['name'] = ['contains']


class BillFilter(django_filters.FilterSet):
    class Meta:
        model = Bill
        fields = {}
        fields['name'] = ['contains']
