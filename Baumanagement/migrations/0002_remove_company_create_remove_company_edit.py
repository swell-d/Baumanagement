# Generated by Django 4.0.3 on 2022-03-15 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='create',
        ),
        migrations.RemoveField(
            model_name='company',
            name='edit',
        ),
    ]