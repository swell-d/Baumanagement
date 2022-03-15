from django.db import models


class CompanyRole(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=512)
    contact = models.CharField(max_length=512)
    email = models.CharField(max_length=512)
    tel = models.CharField(max_length=512)
    address = models.CharField(max_length=512)
    role = models.ForeignKey(CompanyRole, on_delete=models.CASCADE)
    create = models.DateTimeField('create')
    edit = models.DateTimeField('last edit')

    def __str__(self):
        return self.name
