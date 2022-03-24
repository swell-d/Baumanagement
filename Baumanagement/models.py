from django.db import models
from django.db.models import Sum, Q, F, Case, When


def filter_queryset(queryset, request):
    search = request.GET.get('search')
    if search is not None:
        qs = Q()
        for query in [Q(**{f'{field}__icontains': search}) for field in queryset[0].__class__.search_fields()]:
            qs = qs | query
        queryset = queryset.filter(qs)
    return queryset


class CompanyRole(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Rolle')
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Rolle'
        verbose_name_plural = 'Rollen'

    def __str__(self):
        return self.name

    @property
    def count_companies(self):
        return self.companies.count()


class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Hinzugefügt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Geändert')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Firmenname')
    address = models.CharField(max_length=256, null=False, blank=True, verbose_name='Adresse')
    city = models.CharField(max_length=256, null=False, blank=True, verbose_name='PLZ Stadt')
    land = models.CharField(max_length=256, null=False, blank=True, verbose_name='Land', default='Deutschland')
    email = models.EmailField(null=False, blank=True, verbose_name='E-Mail')
    phone = models.CharField(max_length=256, null=False, blank=True, verbose_name='Rufnummer')
    role = models.ManyToManyField(CompanyRole, blank=False, verbose_name='Rolle', related_name='companies')
    ceo = models.CharField(max_length=256, null=False, blank=True, verbose_name='Geschäftsführer')
    vat_number = models.CharField(max_length=16, null=False, blank=True, verbose_name='VAT-Nummer')
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Unternehmen'
        verbose_name_plural = 'Unternehmen'

    def __str__(self):
        return self.name

    @staticmethod
    def extra_fields(qs):
        return qs.all()

    @staticmethod
    def table_fields():
        return 'name', 'address', 'email', 'phone', 'role', 'ceo', 'vat_number'

    @staticmethod
    def search_fields():
        return 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number'

    @staticmethod
    def form_fields():
        return 'open', 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number', 'role'


class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Hinzugefügt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Geändert')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Projektname')
    code = models.CharField(max_length=256, null=False, blank=False, verbose_name='Kode')
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name='Bauherr',
                                on_delete=models.RESTRICT, related_name='projects')
    address = models.CharField(max_length=256, null=False, blank=False, verbose_name='Adresse')
    city = models.CharField(max_length=256, null=False, blank=False, verbose_name='PLZ Stadt')
    land = models.CharField(max_length=256, null=False, blank=True, verbose_name='Land', default='Deutschland')
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projekte'

    def __str__(self):
        return self.name

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(count_contracts=Sum(Case(When(contracts__open=True, then=1))))

    @staticmethod
    def table_fields():
        return 'created', 'name', 'code', 'company', 'address', 'open', 'count_contracts'

    @staticmethod
    def search_fields():
        return 'name', 'code', 'company__name', 'address', 'city', 'land', 'count_contracts'

    @staticmethod
    def form_fields():
        return 'open', 'name', 'code', 'company', 'address', 'city', 'land'


class Contract(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Hinzugefügt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Geändert')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Auftrag')
    date = models.DateField(null=False, blank=True, verbose_name='Datum')
    project = models.ForeignKey(Project, null=False, blank=False, verbose_name='Projekt',
                                on_delete=models.RESTRICT, related_name='contracts')
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name='Bearbeiter',
                                on_delete=models.RESTRICT, related_name='contracts')
    amount_netto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                       verbose_name='Nettobetrag')
    vat = models.FloatField(null=False, blank=False, verbose_name='MWSt')
    amount_brutto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                        verbose_name='Bruttobetrag')
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Auftrag'
        verbose_name_plural = 'Aufträge'

    def __str__(self):
        return self.name

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(payed=Sum(Case(When(payments__open=True, then='payments__amount_brutto')), distinct=True)) \
            .annotate(due=Sum(Case(When(bills__open=True, then='bills__amount_brutto')), distinct=True))

    @staticmethod
    def table_fields():
        return 'created', 'project', 'company', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto', 'due', 'payed'

    @staticmethod
    def search_fields():
        return 'project__name', 'company__name', 'name', 'amount_netto', 'vat', 'amount_brutto', 'due', 'payed'

    @staticmethod
    def form_fields():
        return 'open', 'project', 'company', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'


class Bill(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Hinzugefügt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Geändert')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Rechnung')
    date = models.DateField(null=False, blank=True, verbose_name='Datum')
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name='Auftrag',
                                 on_delete=models.RESTRICT, related_name='bills')
    amount_netto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                       verbose_name='Nettobetrag')
    vat = models.FloatField(null=False, blank=False, verbose_name='MWSt')
    amount_brutto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                        verbose_name='Bruttobetrag')
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Rechnung'
        verbose_name_plural = 'Rechnungen'

    def __str__(self):
        return self.name

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(project=F('contract__project__name'), company=F('contract__company__name'))

    @staticmethod
    def table_fields():
        return 'created', 'project', 'company', 'contract', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'

    @staticmethod
    def search_fields():
        return 'project', 'company', 'contract__name', 'name', 'amount_netto', 'vat', 'amount_brutto'

    @staticmethod
    def form_fields():
        return 'open', 'contract', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'


class Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Hinzugefügt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Geändert')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Zahlung')
    date = models.DateField(null=False, blank=True, verbose_name='Datum')
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name='Auftrag',
                                 on_delete=models.RESTRICT, related_name='payments')
    amount_netto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                       verbose_name='Nettobetrag')
    vat = models.FloatField(null=False, blank=False, verbose_name='MWSt')
    amount_brutto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                                        verbose_name='Bruttobetrag')
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Zahlung'
        verbose_name_plural = 'Zahlungen'

    def __str__(self):
        return self.name

    @staticmethod
    def extra_fields(qs):
        return qs.annotate(project=F('contract__project__name'), company=F('contract__company__name'))

    @staticmethod
    def table_fields():
        return 'created', 'project', 'company', 'contract', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'

    @staticmethod
    def search_fields():
        return 'project', 'company', 'contract__name', 'name', 'amount_netto', 'vat', 'amount_brutto'

    @staticmethod
    def form_fields():
        return 'open', 'contract', 'name', 'date', 'amount_netto', 'vat', 'amount_brutto'
