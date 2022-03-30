from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from Baumanagement.models.models import Payment, Contract, Project
from Baumanagement.tables import PaymentTable
from Baumanagement.views.views import myrender, generate_objects_table, generate_object_table, \
    generate_next_objects_table

baseClass = Payment
tableClass = PaymentTable


class FormClass(ModelForm):
    class Meta:
        model = baseClass
        fields = baseClass.form_fields


def objects_table(request):
    context = {'titel1': _('All payments')}
    generate_objects_table(request, context, baseClass, tableClass, FormClass)
    return myrender(request, context)


def object_table(request, id):
    queryset = baseClass.objects.filter(id=id)
    context = {'titel1': f'{_("Payment")} - {queryset.first().name}', 'tables': []}
    generate_object_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def contract_payments(request, id):
    contract = Contract.objects.get(id=id)
    context = {'titel1': f'{_("Payments")} - {_("Contract")} - {contract.name}'}
    queryset = baseClass.objects.filter(contract=contract)
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def project_payments(request, id):
    project = Project.objects.get(id=id)
    context = {'titel1': f'{_("Payments")} - {_("Project")} - {project.name}'}
    queryset = baseClass.objects.filter(contract__in=project.contracts.all())
    generate_objects_table(request, context, baseClass, tableClass, FormClass, queryset)
    return myrender(request, context)


def generate_payments_by_queryset(request, context, queryset):
    generate_next_objects_table(request, context, baseClass, tableClass, FormClass, queryset, _("Payments"))
