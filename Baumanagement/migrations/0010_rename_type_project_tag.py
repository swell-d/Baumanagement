# Generated by Django 4.0.3 on 2022-04-08 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0009_contract_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='type',
            new_name='tag',
        ),
    ]
