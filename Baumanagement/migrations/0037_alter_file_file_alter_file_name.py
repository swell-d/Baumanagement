# Generated by Django 4.0.3 on 2022-03-25 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0036_alter_file_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='%Y/%m/%d', verbose_name='Datei'),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Name'),
        ),
    ]
