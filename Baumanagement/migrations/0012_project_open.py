# Generated by Django 4.0.3 on 2022-03-16 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0011_alter_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='open',
            field=models.BooleanField(default=1, verbose_name='Aktiv'),
            preserve_default=False,
        ),
    ]
