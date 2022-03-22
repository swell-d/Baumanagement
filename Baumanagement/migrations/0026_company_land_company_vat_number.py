# Generated by Django 4.0.3 on 2022-03-22 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0025_remove_bill_amount_remove_contract_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='land',
            field=models.CharField(blank=True, default='Deutschland', max_length=256, verbose_name='Land'),
        ),
        migrations.AddField(
            model_name='company',
            name='vat_number',
            field=models.CharField(blank=True, max_length=16, verbose_name='VAT-Nummer'),
        ),
    ]