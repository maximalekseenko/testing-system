# Generated by Django 4.0.3 on 2022-03-15 12:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_alter_group_creation_date_alter_moduledata_deadline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 15, 12, 31, 57, 90492, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='moduledata',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 15, 12, 31, 57, 88988, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usermark',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 15, 12, 31, 57, 88310, tzinfo=utc)),
        ),
    ]
