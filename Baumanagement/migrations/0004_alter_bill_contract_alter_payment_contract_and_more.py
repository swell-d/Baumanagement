# Generated by Django 4.0.4 on 2022-05-04 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
        ('Baumanagement', '0003_remove_contract_author_remove_contract_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='bills', to='contracts.contract', verbose_name='Contract'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments', to='contracts.contract', verbose_name='Contract'),
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
        migrations.DeleteModel(
            name='ContractLabel',
        ),
        migrations.DeleteModel(
            name='ContractProduct',
        ),
    ]