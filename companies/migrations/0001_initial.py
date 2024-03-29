# Generated by Django 4.0.4 on 2022-05-04 13:32

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None)),
                ('path', models.TextField(blank=True, max_length=256, null=True, unique=True, verbose_name='Full path')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companylabel_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='children', to='companies.companylabel', verbose_name='Classify label under')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companylabel_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Label',
                'verbose_name_plural': 'Labels',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('address', models.CharField(blank=True, max_length=256, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=256, verbose_name='City')),
                ('land', models.CharField(blank=True, default='Deutschland', max_length=256, verbose_name='Land')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Company name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=256, verbose_name='Phone')),
                ('ceo', models.CharField(blank=True, max_length=256, verbose_name='CEO')),
                ('vat_number', models.CharField(blank=True, max_length=16, verbose_name='VAT number')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('label', models.ManyToManyField(blank=True, related_name='companies', to='companies.companylabel', verbose_name='Labels')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
    ]
