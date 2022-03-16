from django.db import models


class CompanyRole(models.Model):
    name = models.CharField(max_length=512, null=False, blank=False, verbose_name='Rolle')

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Firmenname')
    address = models.CharField(max_length=256, verbose_name='Adresse')
    city = models.CharField(max_length=256, verbose_name='PLZ Stadt')
    email = models.EmailField(verbose_name='E-Mail')
    tel = models.CharField(max_length=128, verbose_name='Rufnummer')
    role = models.ManyToManyField(CompanyRole, verbose_name='Rolle')
    ceo = models.CharField(max_length=256, verbose_name='Geschäftsführer')

    def __str__(self):
        return self.name
