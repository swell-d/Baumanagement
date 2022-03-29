# Generated by Django 4.0.3 on 2022-03-29 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0042_remove_file_bill_remove_file_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='files',
            field=models.JSONField(blank=True, default=[], null=True, verbose_name='Files'),
        ),
        migrations.AddField(
            model_name='company',
            name='files',
            field=models.JSONField(blank=True, default=[], null=True, verbose_name='Files'),
        ),
        migrations.AddField(
            model_name='contract',
            name='files',
            field=models.JSONField(blank=True, default=[], null=True, verbose_name='Files'),
        ),
        migrations.AddField(
            model_name='payment',
            name='files',
            field=models.JSONField(blank=True, default=[], null=True, verbose_name='Files'),
        ),
        migrations.AddField(
            model_name='project',
            name='files',
            field=models.JSONField(blank=True, default=[], null=True, verbose_name='Files'),
        ),
    ]
