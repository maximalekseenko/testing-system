# Generated by Django 3.1.5 on 2021-01-29 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='test1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val1', models.IntegerField(default=0)),
                ('val2', models.BooleanField(default=False)),
            ],
        ),
    ]