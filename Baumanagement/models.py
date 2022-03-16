from django.db import models


class CompanyRole(models.Model):
    name = models.CharField(max_length=512, null=False, blank=False, verbose_name='Rolle')

    def __str__(self):
        return self.name

    @staticmethod
    def fields():
        return 'name', 'anzahl'


class Company(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Firmenname')
    address = models.CharField(max_length=256, verbose_name='Adresse')
    city = models.CharField(max_length=256, verbose_name='PLZ Stadt')
    email = models.EmailField(verbose_name='E-Mail')
    phone = models.CharField(max_length=128, verbose_name='Rufnummer')
    role = models.ManyToManyField(CompanyRole, verbose_name='Rolle', related_name='role')
    ceo = models.CharField(max_length=256, verbose_name='Geschäftsführer')

    def __str__(self):
        return self.name

    @staticmethod
    def fields():
        return 'name', 'address', 'city', 'email', 'phone', 'role', 'ceo'
