# Generated by Django 4.0.3 on 2022-03-30 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0053_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='name',
        ),
    ]
