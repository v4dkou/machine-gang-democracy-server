# -*- coding: utf-8 -*-
import logging

from notifications.fcm import send_fcm_push

logger = logging.getLogger(__name__)


def send_push(user, title=None, text=None, data=None):
    for device in user.userdevice_set.order_by('-date_created'):
        try:
            sent = send_fcm_push(device.device_id, title=None, text=text, data=data)
        except Exception as e:
            print(e)
            continue

        if not sent:
            device.delete()


def notify_chat_new_message(chat, message):
    pass
