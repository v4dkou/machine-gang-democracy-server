from django.contrib import admin

from chats import models as m


class MessageInline(admin.TabularInline):
    model = m.Message
    fields = ('user', 'text', 'date_created', )
    readonly_fields = ('date_created', )
    ordering = ('date_created', )
    extra = 1


@admin.register(m.Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = (MessageInline, )
