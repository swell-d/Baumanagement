# Generated by Django 4.0.3 on 2022-03-25 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0034_alter_bill_date_alter_bill_vat_alter_contract_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='files', to='Baumanagement.payment', verbose_name='Datei'),
        ),
    ]
