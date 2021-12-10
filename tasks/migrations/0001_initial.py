# Generated by Django 3.2.4 on 2021-12-10 12:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Имя', max_length=64)),
                ('content', models.CharField(default='Условие', max_length=512)),
                ('answer', models.IntegerField(default=0)),
                ('options', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('name', models.CharField(default='Новый модуль', max_length=64)),
                ('description', models.CharField(default='AAAA', max_length=256)),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2021, 12, 10, 12, 14, 31, 99156, tzinfo=utc))),
                ('tasks', models.JSONField(default={})),
                ('is_public', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('key', models.CharField(default='AAAAAAAAAAAAAAAA', max_length=16, primary_key=True, serialize=False, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
