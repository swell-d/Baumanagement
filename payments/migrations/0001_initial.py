# Generated by Django 4.0.4 on 2022-05-04 13:32

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bank_accounts', '0001_initial'),
        ('contracts', '0001_initial'),
    ]

    operations = [
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
                ('account_from', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments_from', to='bank_accounts.account', verbose_name='Write-off account')),
                ('account_to', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments_to', to='bank_accounts.account', verbose_name='Top-up account')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments', to='contracts.contract', verbose_name='Contract')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
