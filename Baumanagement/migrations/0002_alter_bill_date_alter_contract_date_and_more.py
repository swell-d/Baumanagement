# Generated by Django 4.0.3 on 2022-04-06 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Date'),
        ),
    ]