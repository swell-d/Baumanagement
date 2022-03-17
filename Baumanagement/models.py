from django.db import models


class CompanyRole(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Rolle')

    class Meta:
        verbose_name = 'Rolle'
        verbose_name_plural = 'Rollen'

    def __str__(self):
        return self.name

    @staticmethod
    def fields():
        return 'name',

    def count_companies(self):
        return self.companies.all().count()


class Company(models.Model):
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
        return 'name', 'address', 'city', 'email', 'phone', 'role', 'ceo'

    def save(self, *args, **kwargs):
        CompanyRole.count_companies()
        return super(Company, self).save(*args, **kwargs)


class Project(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Projekt')
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

    @staticmethod
    def fields():
        return 'name', 'code', 'company', 'address', 'city', 'open'


class Contract(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Auftrag')
    project = models.ForeignKey(Project, null=False, blank=False, verbose_name='Projekt',
                                on_delete=models.RESTRICT, related_name='contracts')
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name='Bearbeiter',
                                on_delete=models.RESTRICT, related_name='contracts')

    class Meta:
        verbose_name = 'Auftrag'
        verbose_name_plural = 'Aufträge'

    def __str__(self):
        return self.name

    @staticmethod
    def fields():
        return 'name', 'project', 'company', 'payments'

    def payed(self):
        return sum(payment.amount for payment in self.payments.all())


class Payment(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Beschreibung')
    contract = models.ForeignKey(Contract, null=False, blank=False, verbose_name='Auftrag',
                                 on_delete=models.RESTRICT, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False, verbose_name='Betrag')

    class Meta:
        verbose_name = 'Zahlung'
        verbose_name_plural = 'Zahlungen'

    def __str__(self):
        return self.name

    @staticmethod
    def fields():
        return 'name', 'contract', 'amount'
