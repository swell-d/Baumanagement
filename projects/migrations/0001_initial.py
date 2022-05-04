# Generated by Django 4.0.4 on 2022-05-04 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projectlabel_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='children', to='projects.projectlabel', verbose_name='Classify label under')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projectlabel_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Label',
                'verbose_name_plural': 'Labels',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('comment_ids', models.JSONField(blank=True, default=list, verbose_name='Comments')),
                ('address', models.CharField(blank=True, max_length=256, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=256, verbose_name='City')),
                ('land', models.CharField(blank=True, default='Deutschland', max_length=256, verbose_name='Land')),
                ('file_ids', models.JSONField(blank=True, default=list, verbose_name='Files')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Project name')),
                ('code', models.CharField(blank=True, max_length=256, verbose_name='Code')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='projects', to='companies.company', verbose_name='Company')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='projects', to='projects.projectlabel', verbose_name='Label')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
    ]
