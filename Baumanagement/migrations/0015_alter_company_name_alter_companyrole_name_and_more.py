# Generated by Django 4.0.3 on 2022-04-08 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0014_alter_contract_tag_alter_project_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Company name'),
        ),
        migrations.AlterField(
            model_name='companyrole',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='contracttag',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(max_length=3, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(default='', max_length=3, unique=True, verbose_name='Symbol'),
        ),
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.CharField(blank=True, max_length=256, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Project name'),
        ),
        migrations.AlterField(
            model_name='projecttag',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Type'),
        ),
    ]
