# Generated by Django 4.0.3 on 2022-04-11 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0023_alter_contracttag_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttag',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Baumanagement.projecttag', verbose_name='Classify label under'),
        ),
    ]
