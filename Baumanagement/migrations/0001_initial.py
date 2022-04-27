# Generated by Django 4.0.4 on 2022-04-27 13:01

import Baumanagement.models.models_currency
from decimal import Decimal
from django.conf import settings
import django.core.validators
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
                ('bank', models.CharField(blank=True, max_length=256, verbose_name='Bank')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
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
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Company name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=256, verbose_name='Phone')),
                ('ceo', models.CharField(blank=True, max_length=256, verbose_name='CEO')),
                ('vat_number', models.CharField(blank=True, max_length=16, verbose_name='VAT number')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
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
                ('amount_netto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount netto')),
                ('amount_brutto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount brutto')),
                ('vat', models.FloatField(default=19, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='VAT %')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, verbose_name='Contract name')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], default='buy', max_length=4, verbose_name='Contract type')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contracts', to='Baumanagement.company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Contract',
                'verbose_name_plural': 'Contracts',
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
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=3, unique=True, verbose_name='Code')),
                ('symbol', models.CharField(max_length=3, unique=True, verbose_name='Symbol')),
                ('rate', models.FloatField(default=1, verbose_name='Rate')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currency_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currency_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
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
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Project name')),
                ('code', models.CharField(blank=True, max_length=256, verbose_name='Code')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='projects', to='Baumanagement.company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='SearchQueries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(max_length=256, verbose_name='Page')),
                ('query', models.CharField(max_length=256, verbose_name='Query')),
                ('count', models.BigIntegerField(default=0, verbose_name='Visits')),
            ],
            options={
                'verbose_name': 'Search query',
                'verbose_name_plural': 'Search queries',
            },
        ),
        migrations.CreateModel(
            name='Visits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(max_length=256, unique=True, verbose_name='Page')),
                ('count', models.BigIntegerField(default=0, verbose_name='Visits')),
            ],
            options={
                'verbose_name': 'Visits',
                'verbose_name_plural': 'Visits',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateTimeField(blank=True, null=True)),
                ('date_to', models.DateTimeField(blank=True, null=True)),
                ('sort', models.JSONField(blank=True, default=dict, null=True)),
                ('img', models.ImageField(null=True, upload_to='', verbose_name='Image')),
                ('active_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='settings', to='Baumanagement.project')),
                ('default_currency', models.ForeignKey(default=Baumanagement.models.models_currency.Currency.get_EUR_id, on_delete=django.db.models.deletion.RESTRICT, to='Baumanagement.currency')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='ProjectTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projecttag_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='children', to='Baumanagement.projecttag', verbose_name='Classify label under')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projecttag_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='projects', to='Baumanagement.projecttag', verbose_name='Tag'),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productcategory_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='children', to='Baumanagement.productcategory', verbose_name='Classify category under')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productcategory_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('amount_netto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount netto')),
                ('amount_brutto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount brutto')),
                ('vat', models.FloatField(default=19, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='VAT %')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('code', models.CharField(blank=True, max_length=256, verbose_name='Code')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('type', models.CharField(choices=[('Product', 'Product'), ('Service', 'Service')], default='Product', max_length=7, verbose_name='Product type')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('categories', models.ManyToManyField(blank=True, related_name='products', to='Baumanagement.productcategory', verbose_name='Categories')),
                ('currency', models.ForeignKey(default=Baumanagement.models.models_currency.Currency.get_EUR_id, on_delete=django.db.models.deletion.RESTRICT, related_name='products', to='Baumanagement.currency', verbose_name='Currency')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
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
                ('amount_netto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount netto')),
                ('amount_brutto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount brutto')),
                ('vat', models.FloatField(default=19, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='VAT %')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, verbose_name='Payment name')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('account_from', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments_from', to='Baumanagement.account', verbose_name='Write-off account')),
                ('account_to', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments_to', to='Baumanagement.account', verbose_name='Top-up account')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments', to='Baumanagement.contract', verbose_name='Contract')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='MyMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('name', models.TextField(verbose_name='Message')),
                ('level', models.IntegerField(verbose_name='Level')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mymessage_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mymessage_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
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
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
        migrations.CreateModel(
            name='ContractTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracttag_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='children', to='Baumanagement.contracttag', verbose_name='Classify label under')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracttag_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='contract',
            name='currency',
            field=models.ForeignKey(default=Baumanagement.models.models_currency.Currency.get_EUR_id, on_delete=django.db.models.deletion.RESTRICT, related_name='contracts', to='Baumanagement.currency', verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='contract',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contracts', to='Baumanagement.project', verbose_name='Project'),
        ),
        migrations.AddField(
            model_name='contract',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contracts', to='Baumanagement.contracttag', verbose_name='Tag'),
        ),
        migrations.AddField(
            model_name='contract',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
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
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contacts', to='Baumanagement.company', verbose_name='Company')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
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
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Role')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companyrole_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companyrole_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
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
        migrations.AddField(
            model_name='company',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
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
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
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
                ('amount_netto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount netto')),
                ('amount_brutto_positiv', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount brutto')),
                ('vat', models.FloatField(default=19, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='VAT %')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, verbose_name='Bill name')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='bills', to='Baumanagement.contract', verbose_name='Contract')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
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
            name='currency',
            field=models.ForeignKey(default=Baumanagement.models.models_currency.Currency.get_EUR_id, on_delete=django.db.models.deletion.RESTRICT, related_name='accounts', to='Baumanagement.currency', verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='account',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
    ]
