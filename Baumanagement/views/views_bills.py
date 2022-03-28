from django.contrib import messages
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_tables2 import RequestConfig

from Baumanagement.models.models import Bill, Contract, Project
from Baumanagement.models.abstract import add_search_field
from Baumanagement.tables import BillTable
from Baumanagement.views.views import myrender, upload_files


def bills(request):
    context = {'titel1': _('All bills')}
    form_new_bill(request, context)

    queryset = Bill.extra_fields(Bill.objects)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def contract_bills(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'{_("Bills")} - {_("Contract")} - {contract.name}'}
    form_new_bill(request, context)

    queryset = Bill.objects.filter(contract=contract)
    queryset = Bill.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def project_bills(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Bills")} - {_("Project")} - {project.name}'}
    form_new_bill(request, context)

    queryset = Bill.objects.filter(contract__in=project.contracts.all())
    queryset = Bill.extra_fields(queryset)
    queryset = add_search_field(queryset, request, context)
    table1 = BillTable(queryset, order_by="id")
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


def bill(request, id):
    bill = Bill.objects.get(id=id)
    context = {'titel1': f'{_("Bill")} - {bill.name}', 'tables': []}
    form_edit_bill(request, context, bill)

    queryset = Bill.objects.filter(id=id)
    queryset = Bill.extra_fields(queryset)
    table1 = BillTable(queryset)
    RequestConfig(request).configure(table1)
    context['table1'] = table1

    return myrender(request, context)


class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = Bill.form_fields()


def form_new_bill(request, context):
    if request.method == 'POST':
        formset = BillForm(request.POST, request.FILES)
        if formset.is_valid():
            new_object = Bill(**formset.cleaned_data)
            new_object.save()
            messages.success(request, f'{new_object.name} {_("created")}')
            upload_files(request, bill=new_object)
    context['form'] = BillForm()
    context['files_form'] = []
    context['buttons'] = ['New']


def form_edit_bill(request, context, bill):
    if request.method == 'POST':
        formset = BillForm(request.POST, request.FILES, instance=bill)
        if formset.is_valid():
            bill.save()
            messages.success(request, f'{bill.name} {_("changed")}')
            upload_files(request, bill=bill)
    context['form'] = BillForm(instance=bill)
    context['files_form'] = bill.files.all()
    context['buttons'] = ['Edit']
