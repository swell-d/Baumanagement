from decimal import Decimal

from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Case, When
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models_company import Company
from Baumanagement.models.models_currency import Currency
from Baumanagement.models.models_projects import Project
from bills.views import contract_bills_qs, generate_bills_by_queryset
from contracts.models import Contract, ContractLabel
from contracts.tables import ContractTable
from main.views import get_base_context, generate_objects_table, myrender, generate_object_table, \
    generate_next_objects_table
from notifications.models import Notification
from payments.views import contract_payments_qs, generate_payments_by_queryset

baseClass = Contract
tableClass = ContractTable


class FormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(open=True)
        self.fields['company'].queryset = Company.objects.filter(open=True)
        self.fields['currency'].queryset = Currency.objects.filter(open=True)
        self.fields['currency'].initial = Currency.objects.get(code='EUR')

    class Meta:
        model = baseClass
        fields = baseClass.form_fields
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}


def tags():
    html = f'<a href="" onclick="mainTableLabel(&quot;&quot;);return false;">{_("All")}</a>, '
    html += ', '.join(
        f'#<a href="" onclick="mainTableLabel(&quot;{tag.id}&quot;);return false;">{str(tag)}</a>'
        for tag in ContractLabel.objects.order_by('name') if tag.count > 0)
    html += ' &#9881;<a href="' + reverse('contractlabels') + '">' + _('Manage labels') + '</a>'
    return format_html(html)


@login_required
def objects_table(request):
    context = get_base_context(request)
    context['tags1'] = tags()
    queryset = qs_annotate(baseClass.objects)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


@login_required
def object_table(request, id):
    context = get_base_context(request)
    queryset = baseClass.objects.filter(id=id)
    if queryset.first() is None:
        raise Http404
    queryset = queryset.annotate(amount_netto=F('amount_netto_positiv'),
                                 amount_brutto=F('amount_brutto_positiv'))
    contract = queryset.first()

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_contracts', args=[contract.project.company.id]),
                               'text': contract.project.company.name},
                              {'link': reverse('project_id_contracts', args=[contract.project.id]),
                               'text': contract.project.name},
                              {'text': contract.name}]

    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)

    disable_children(request, queryset.first())

    bills = contract_bills_qs(contract)
    generate_bills_by_queryset(request, context, bills)

    payments = contract_payments_qs(contract)
    generate_payments_by_queryset(request, context, payments)

    return myrender(request, context)


def disable_children(request, contract):
    if request.method == 'POST' and not contract.open:
        for bill in contract.bills.all():
            if bill.open:
                bill.open = False
                bill.save()

                verbose_name = bill.verbose_name()
                link = reverse(bill.url_id, args=[bill.id])
                Notification.message(
                    request, f'{verbose_name} "<a href="{link}">{bill.name}</a>" ' + _("disabled"), 'WARNING'
                )

        for payment in contract.payments.all():
            if payment.open:
                payment.open = False
                payment.save()

                verbose_name = payment.verbose_name()
                link = reverse(payment.url_id, args=[payment.id])
                Notification.message(
                    request, f'{verbose_name} "<a href="{link}">{payment.name}</a>" ' + _("disabled"), 'WARNING'
                )


@login_required
def company_contracts(request, id):
    context = get_base_context(request)
    company = get_object_or_404(Company, id=id)
    context['tags1'] = tags()
    queryset = company_contracts_qs(company)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'text': company.name}]

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def company_contracts_qs(company):
    return qs_annotate(baseClass.objects.filter(Q(project__company=company) | Q(company=company)))


@login_required
def project_contracts(request, id):
    context = get_base_context(request)
    project = get_object_or_404(Project, id=id)
    context['tags1'] = tags()
    queryset = project_contracts_qs(project)

    context['breadcrumbs'] = [{'link': reverse(baseClass.urls), 'text': _("All")},
                              {'link': reverse('company_id_contracts', args=[project.company.id]),
                               'text': project.company.name},
                              {'text': project.name}]

    form = FormClass()
    form.fields["project"].initial = project
    form.fields['project'].queryset = Project.objects.filter(id=id)
    context['form'] = form

    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def project_contracts_qs(project):
    return qs_annotate(project.contracts)


def generate_contracts_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, queryset)


def qs_annotate(queryset):
    return queryset.annotate(
        amount_netto=Case(When(type=Contract.BUY, then=-F('amount_netto_positiv')),
                          When(type=Contract.SELL, then='amount_netto_positiv'),
                          default=Decimal(0))).annotate(
        amount_brutto=Case(When(type=Contract.BUY, then=-F('amount_brutto_positiv')),
                           When(type=Contract.SELL, then='amount_brutto_positiv'),
                           default=Decimal(0)))
