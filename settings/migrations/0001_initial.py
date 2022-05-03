# Generated by Django 4.0.3 on 2022-05-03 21:02

import Baumanagement.models.models_currency
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Baumanagement', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateTimeField(blank=True, null=True)),
                ('date_to', models.DateTimeField(blank=True, null=True)),
                ('sort', models.JSONField(blank=True, default=dict, null=True)),
                ('img', models.ImageField(null=True, upload_to='', verbose_name='Image')),
                ('datetime_format', models.CharField(default='%d.%m.%Y %H:%M', max_length=256, verbose_name='Datetime format')),
                ('date_format', models.CharField(default='%d.%m.%y', max_length=256, verbose_name='Date format')),
                ('active_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='settings', to='Baumanagement.project')),
                ('default_currency', models.ForeignKey(default=Baumanagement.models.models_currency.Currency.get_EUR_id, on_delete=django.db.models.deletion.RESTRICT, to='Baumanagement.currency')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]