# Generated by Django 4.0.3 on 2022-04-06 16:32

import datetime
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
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
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
                ('name', models.CharField(max_length=256, verbose_name='Company name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=256, verbose_name='Phone')),
                ('ceo', models.CharField(blank=True, max_length=256, verbose_name='CEO')),
                ('vat_number', models.CharField(blank=True, max_length=16, verbose_name='VAT number')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('amount_netto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount netto')),
                ('amount_brutto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount brutto')),
                ('amount_netto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount netto')),
                ('vat', models.FloatField(default=19, verbose_name='VAT %')),
                ('amount_brutto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount brutto')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, verbose_name='Contract name')),
                ('date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Date')),
                ('type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], default='buy', max_length=4, verbose_name='Contract type')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contracts', to='Baumanagement.company', verbose_name='Company')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contract',
                'verbose_name_plural': 'Contracts',
            },
        ),
        migrations.CreateModel(
            name='Project',
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
                ('name', models.CharField(max_length=256, verbose_name='Project name')),
                ('code', models.CharField(blank=True, max_length=256, verbose_name='Code')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='projects', to='Baumanagement.company', verbose_name='Company')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('amount_netto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount netto')),
                ('amount_brutto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount brutto')),
                ('amount_netto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount netto')),
                ('vat', models.FloatField(default=19, verbose_name='VAT %')),
                ('amount_brutto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount brutto')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, verbose_name='Payment name')),
                ('date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Date')),
                ('account_from', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='bills_from', to='Baumanagement.account', verbose_name='Write-off account')),
                ('account_to', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='bills_to', to='Baumanagement.account', verbose_name='Top-up account')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments', to='Baumanagement.contract', verbose_name='Contract')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('file', models.FileField(upload_to='%Y/%m/%d', verbose_name='Files')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('code', models.CharField(max_length=3, verbose_name='Code')),
                ('symbol', models.CharField(default='', max_length=3, verbose_name='Symbol')),
                ('rate', models.FloatField(default=1, verbose_name='Rate')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.AddField(
            model_name='contract',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contracts', to='Baumanagement.currency', verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='contract',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contracts', to='Baumanagement.project', verbose_name='Project'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=256, verbose_name='Phone')),
                ('position', models.CharField(blank=True, max_length=256, verbose_name='Position')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contacts', to='Baumanagement.company', verbose_name='Company')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='CompanyRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('name', models.CharField(max_length=256, verbose_name='Role')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='role',
            field=models.ManyToManyField(related_name='companies', to='Baumanagement.companyrole', verbose_name='Role'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.TextField(verbose_name='Comment')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('amount_netto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount netto')),
                ('amount_brutto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount brutto')),
                ('amount_netto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount netto')),
                ('vat', models.FloatField(default=19, verbose_name='VAT %')),
                ('amount_brutto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount brutto')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, verbose_name='Bill name')),
                ('date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Date')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='bills', to='Baumanagement.contract', verbose_name='Contract')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bill',
                'verbose_name_plural': 'Bills',
            },
        ),
        migrations.AddField(
            model_name='account',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='accounts', to='Baumanagement.company', verbose_name='Company'),
        ),
        migrations.AddField(
            model_name='account',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='accounts', to='Baumanagement.currency', verbose_name='Currency'),
        ),
    ]
