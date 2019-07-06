import json
from django.core.management.base import BaseCommand

from notifications.models import NotificationTemplate


class Command(BaseCommand):
    """
    Creates initial NotificationTemplates.
    """
    help = 'Creates initial NotificationTemplates.'

    def handle(self, *args, **kwargs):
        with open('notifications/management/commands/data/notifications.json') as f:
            notifications = json.load(f)

        for notification in notifications:
            slug = notification.get('slug')

            try:
                NotificationTemplate.objects.get(slug=slug)
                print('notification template for slug {} exists'.format(slug))
            except NotificationTemplate.DoesNotExist:
                NotificationTemplate.objects.create(**notification)
                print('created notification template for slug {}'.format(slug))
