# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from accounts.models import User


class NotificationTemplate(models.Model):
    slug = models.CharField('Слаг', max_length=255, unique=True)
    name = models.CharField('Название', max_length=255)

    variables = ArrayField(models.CharField(max_length=255), verbose_name='Переменные', default=list)
    title_template = models.CharField('Шаблон заголовка', max_length=255)
    template = models.TextField('Шаблон')

    class Meta:
        verbose_name = 'шаблон уведомления'
        verbose_name_plural = 'шаблоны уведомлений'

    def __str__(self):
        return self.name


class Notification(models.Model):
    template = models.ForeignKey(NotificationTemplate, verbose_name='Шаблон', blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, verbose_name='Получатель', on_delete=models.CASCADE)
    message = models.TextField('Сообщение')

    is_read = models.BooleanField('Прочитано', default=False)

    date_created = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ('-date_created', )

    def __str__(self):
        return self.message


class UserDevice(models.Model):
    IOS_DEV = 'ios-dev'
    IOS = 'ios'
    GCM = 'gcm'

    DEVICE_TYPES = (
        (IOS_DEV, 'IOS dev'),
        (IOS, 'IOS'),
        (GCM, 'GCM'),
    )

    user = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE)
    device_type = models.CharField('Device type', max_length=16, choices=DEVICE_TYPES)
    device_id = models.CharField('Device ID', max_length=255)

    date_created = models.DateTimeField('Created', default=timezone.now, editable=False)
