from django.db import models


class CompanyRole(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Rolle')

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
    email = models.EmailField(null=False, blank=True, verbose_name='E-Mail')
    phone = models.CharField(max_length=256, null=False, blank=True, verbose_name='Rufnummer')
    role = models.ManyToManyField(CompanyRole, blank=False, verbose_name='Rolle', related_name='companies')
    ceo = models.CharField(max_length=256, null=False, blank=True, verbose_name='Geschäftsführer')

    class Meta:
        verbose_name = 'Unternehmen'
        verbose_name_plural = 'Unternehmen'

    def __str__(self):
        return self.name

    @staticmethod
    def fields():
        return 'name', 'address', 'email', 'phone', 'role', 'ceo'


class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Hinzugefügt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Geändert')

    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Projektname')
    code = models.CharField(max_length=256, null=False, blank=False, verbose_name='Kode')
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name='Bauherr',
                                on_delete=models.RESTRICT, related_name='projects')
    address = models.CharField(max_length=256, null=False, blank=False, verbose_name='Adresse')
    city = models.CharField(max_length=256, null=False, blank=False, verbose_name='PLZ Stadt')
    open = models.BooleanField(default=True, null=False, blank=False, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projekte'

    def __str__(self):
        return self.name

    @property
    def count_contracts(self):
        return self.contracts.count()

    @staticmethod
    def fields():
        return 'created', 'name', 'code', 'company', 'address', 'open', 'count_contracts'


class Contract(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Hinzugefügt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Geändert')

    date = models.DateField(null=False, blank=True, verbose_name='Datum')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Auftrag')
    project = models.ForeignKey(Project, null=False, blank=False, verbose_name='Projekt',
                                on_delete=models.RESTRICT, related_name='contracts')
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name='Bearbeiter',
                                on_delete=models.RESTRICT, related_name='contracts')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name='Betrag')

    class Meta:
        verbose_name = 'Auftrag'
        verbose_name_plural = 'Aufträge'

    def __str__(self):
        return self.name

    @property
    def due(self):
        return sum(bill.amount for bill in self.bills.all())

    @property
    def payed(self):
        return sum(payment.amount for payment in self.payments.all())

    @staticmethod
    def fields():
        return 'created', 'project', 'company', 'name', 'date', 'amount', 'due', 'payed'


class Bill(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Hinzugefügt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Geändert')

    date = models.DateField(null=False, blank=True, verbose_name='Datum')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Rechnung')
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name='Auftrag',
                                 on_delete=models.RESTRICT, related_name='bills')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name='Betrag')

    class Meta:
        verbose_name = 'Rechnung'
        verbose_name_plural = 'Rechnungen'

    def __str__(self):
        return self.name

    @property
    def project(self):
        return self.contract.project

    @property
    def company(self):
        return self.contract.company

    @staticmethod
    def fields():
        return 'created', 'project', 'company', 'contract', 'name', 'date', 'amount'


class Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Hinzugefügt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Geändert')

    date = models.DateField(null=False, blank=True, verbose_name='Datum')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Zahlung')
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name='Auftrag',
                                 on_delete=models.RESTRICT, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name='Betrag')

    class Meta:
        verbose_name = 'Zahlung'
        verbose_name_plural = 'Zahlungen'

    def __str__(self):
        return self.name

    @property
    def project(self):
        return self.contract.project

    @property
    def company(self):
        return self.contract.company

    @staticmethod
    def fields():
        return 'created', 'project', 'company', 'contract', 'name', 'date', 'amount'
