# Generated by Django 3.2.4 on 2021-12-18 19:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('name', models.CharField(default='', max_length=32)),
                ('description', models.CharField(default='', max_length=1024)),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2021, 12, 18, 19, 8, 33, 209075, tzinfo=utc))),
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False, unique=True)),
                ('moduls_data', models.JSONField(default={})),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('mem', models.ManyToManyField(blank=True, related_name='mem', to=settings.AUTH_USER_MODEL)),
                ('mem_adm', models.ManyToManyField(blank=True, related_name='mem_adm', to=settings.AUTH_USER_MODEL)),
                ('mem_req', models.ManyToManyField(blank=True, related_name='mem_req', to=settings.AUTH_USER_MODEL)),
                ('moduls', models.ManyToManyField(blank=True, related_name='moduls', to='tasks.Module')),
            ],
        ),
    ]
