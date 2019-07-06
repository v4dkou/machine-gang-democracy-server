# Send to single device.
from pyfcm import FCMNotification
from django.conf import settings


def send_fcm_push(device_id, title=None, text=None, data=None):
    push_service = FCMNotification(api_key=settings.FCM_API_KEY)

    result = push_service.notify_single_device(registration_id=device_id, message_title=title, message_body=text, data_message=data)

    return result.get('success')
