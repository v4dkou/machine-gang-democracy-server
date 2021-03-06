# Generated by Django 2.2.3 on 2019-07-06 09:08

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=255, unique=True, verbose_name='Слаг')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('variables', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=list, size=None, verbose_name='Переменные')),
                ('title_template', models.CharField(max_length=255, verbose_name='Шаблон заголовка')),
                ('template', models.TextField(verbose_name='Шаблон')),
            ],
            options={
                'verbose_name': 'шаблон уведомления',
                'verbose_name_plural': 'шаблоны уведомлений',
            },
        ),
        migrations.CreateModel(
            name='UserDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(choices=[('ios-dev', 'IOS dev'), ('ios', 'IOS'), ('gcm', 'GCM')], max_length=16, verbose_name='Device type')),
                ('device_id', models.CharField(max_length=255, verbose_name='Device ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('is_read', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notifications.NotificationTemplate', verbose_name='Шаблон')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
                'ordering': ('-date_created',),
            },
        ),
    ]
