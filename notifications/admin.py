# -*- coding: utf-8 -*-
from django.contrib import admin
from notifications.models import NotificationTemplate, Notification, UserDevice


# Register your models here.
@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = ('variables', )
    readonly_fields = ('slug', 'variables', )






@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    pass

