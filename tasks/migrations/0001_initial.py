from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id',              models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title',           models.CharField(default='Задание', max_length=64)),
                ('author',          models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('content',         models.CharField(default='', max_length=512)),
                # answers
                ('correct_answer',  models.CharField(default='', max_length=32)),
                ('options_answer',  models.ManyToManyField(to='tasks.Answer')),
                ('answer_type',     models.CharField(default='', max_length=32)),
                ('marks',           models.ManyToManyField(to='tasks.Mark')),
                # other
                ('creation_date',   models.DateTimeField(auto_now_add=True)), ], ),

        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id',              models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author',          models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('mark',            models.CharField(default='', max_length=16)),
                ('comment',         models.CharField(default='', max_length=32)), ], ),

        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id',              models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author',          models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('content',         models.CharField(default='', max_length=32)), ], ),

        migrations.CreateModel(
            name='Module',
            fields=[
                ('id',              models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',            models.CharField(default='Новый модуль', max_length=64)),
                ('tasks',           models.ManyToManyField(to='tasks.Task')), ], ), ]
