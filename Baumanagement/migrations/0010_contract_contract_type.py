# Generated by Django 4.0.3 on 2022-04-03 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0009_contracttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='contract_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='contracts', to='Baumanagement.contracttype', verbose_name='Contract type'),
        ),
    ]
