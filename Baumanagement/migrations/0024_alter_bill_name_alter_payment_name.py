# Generated by Django 4.0.3 on 2022-03-21 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0023_contract_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Rechnung'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Zahlung'),
        ),
    ]