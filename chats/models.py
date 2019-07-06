from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Chat(models.Model):
    name = models.CharField('Name', max_length=255, blank=True, null=True)


class Message(models.Model):
    user = models.ForeignKey('accounts.User', related_name='messages', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField('Text')

    date_created = models.DateTimeField('Created', default=timezone.now, editable=False)
