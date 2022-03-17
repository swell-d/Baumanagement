# Generated by Django 4.0.3 on 2022-03-16 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0014_alter_project_open'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Beschreibung')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Betrag')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments', to='Baumanagement.contract', verbose_name='Auftrag')),
            ],
            options={
                'verbose_name': 'Zahlung',
                'verbose_name_plural': 'Zahlungen',
            },
        ),
    ]
