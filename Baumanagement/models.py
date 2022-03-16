from django.db import models


class CompanyRole(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Rolle')
    count = models.IntegerField(null=False, blank=False, verbose_name='Anzahl')

    def __str__(self):
        return self.name

    @staticmethod
    def fields():
        return 'name', 'count'

    @classmethod
    def count_companies(cls):
        for each in cls.objects.all():
            new_count = Company.objects.filter(role=each.id).count()
            if each.count != new_count:
                each.count = new_count
                each.save()


class Company(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Firmenname')
    address = models.CharField(max_length=256, null=False, blank=True, verbose_name='Adresse')
    city = models.CharField(max_length=256, null=False, blank=True, verbose_name='PLZ Stadt')
    email = models.EmailField(null=False, blank=True, verbose_name='E-Mail')
    phone = models.CharField(max_length=256, null=False, blank=True, verbose_name='Rufnummer')
    role = models.ManyToManyField(CompanyRole, blank=False, verbose_name='Rolle', related_name='companies')
    ceo = models.CharField(max_length=256, null=False, blank=True, verbose_name='Geschäftsführer')

    def __str__(self):
        return self.name

    @staticmethod
    def fields():
        return 'name', 'address', 'city', 'email', 'phone', 'role', 'ceo'


class Project(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Projekt')
    code = models.CharField(max_length=256, null=False, blank=False, verbose_name='Kode')
    company = models.ForeignKey(Company, null=False, blank=False, verbose_name='Bauherr',
                                on_delete=models.RESTRICT, related_name='projects')
    address = models.CharField(max_length=256, null=False, blank=False, verbose_name='Adresse')
    city = models.CharField(max_length=256, null=False, blank=False, verbose_name='PLZ Stadt')

    def __str__(self):
        return self.name

    @staticmethod
    def fields():
        return 'name', 'code', 'company', 'address', 'city'
