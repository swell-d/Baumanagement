# Generated by Django 4.0.3 on 2022-04-11 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0020_alter_contracttag_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contracttag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterModelOptions(
            name='projecttag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AddField(
            model_name='projecttag',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Baumanagement.projecttag'),
        ),
        migrations.AlterField(
            model_name='projecttag',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Name'),
        ),
    ]