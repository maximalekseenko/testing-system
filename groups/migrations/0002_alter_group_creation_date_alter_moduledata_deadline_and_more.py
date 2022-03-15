# Generated by Django 4.0.3 on 2022-03-14 19:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 14, 19, 47, 28, 320422, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='moduledata',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 14, 19, 47, 28, 318027, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usermark',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 14, 19, 47, 28, 316748, tzinfo=utc)),
        ),
    ]
