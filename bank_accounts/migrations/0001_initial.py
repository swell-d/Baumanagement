# Generated by Django 4.0.4 on 2022-05-04 13:32

import currencies.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currencies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, verbose_name='Account name')),
                ('IBAN', models.CharField(blank=True, max_length=256, verbose_name='IBAN')),
                ('BIC', models.CharField(blank=True, max_length=256, verbose_name='BIC')),
                ('bank', models.CharField(blank=True, max_length=256, verbose_name='Bank')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='accounts', to='companies.company', verbose_name='Company')),
                ('currency', models.ForeignKey(default=currencies.models.Currency.get_EUR_id, on_delete=django.db.models.deletion.RESTRICT, related_name='accounts', to='currencies.currency', verbose_name='Currency')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
    ]
