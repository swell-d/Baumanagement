# Generated by Django 4.0.4 on 2022-05-04 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('name', models.TextField(verbose_name='Message')),
                ('level', models.IntegerField(verbose_name='Level')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.DeleteModel(
            name='MyMessage',
        ),
    ]
