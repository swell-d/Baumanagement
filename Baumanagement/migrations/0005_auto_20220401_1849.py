# Generated by Django 4.0.3 on 2022-04-01 16:41

from django.db import migrations


def create_currency(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Currency = apps.get_model("Baumanagement", "Currency")
    eur = Currency.objects.using(db_alias).get_or_create(name='Euro', code='EUR')
    Account = apps.get_model("Baumanagement", "Account")
    for each in Account.objects.using(db_alias).all():
        each.currency = eur[0]
        each.save()


class Migration(migrations.Migration):
    dependencies = [
        ('Baumanagement', '0004_account_currency'),
    ]

    operations = [
        migrations.RunPython(create_currency),
    ]
