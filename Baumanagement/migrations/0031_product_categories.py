# Generated by Django 4.0.3 on 2022-04-11 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Baumanagement', '0030_alter_productcategory_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='products', to='Baumanagement.productcategory', verbose_name='Categories'),
        ),
    ]