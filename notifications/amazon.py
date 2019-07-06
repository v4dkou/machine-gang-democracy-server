import logging
import json
import boto3
from django.conf import settings

logger = logging.getLogger(__name__)


def create_client():
    client_id = settings.AWS_SNS_CLIENT_ID
    secret = settings.AWS_SNS_SECRET
    region = settings.AWS_SNS_REGION

    client = boto3.client(
        "sns",
        aws_access_key_id=client_id,
        aws_secret_access_key=secret,
        region_name=region
    )

    return client





def send_push_ios(device_id, text=None, data=None):
    logger.info('Sending push to {}'.format(device_id))
    assert (text is not None or data is not None)

    client = create_client()

    try:
        endpoint_response = client.create_platform_endpoint(
            PlatformApplicationArn=settings.AWS_IOS_APP_ARN,
            Token=device_id
        )
    except client.exceptions.InvalidParameterException as e:
        logger.error('Invalid device_id {}:\n{}'.format(device_id, e))
        return False

    endpoint_arn = endpoint_response['EndpointArn']
    apns_key = 'APNS'
    apns_dict = {
        'aps': {}
    }

    if data is not None:
        apns_dict.update(data)
        apns_dict['aps']['content-available'] = 1

    if text is not None:
        apns_dict['aps']['alert'] = {
            'body': text
        }

    if settings.AWS_IOS_SANDBOX:
        apns_key = 'APNS_SANDBOX'
        apns_dict['aps']['sound'] = 'default'

    try:
        client.publish(
            TargetArn=endpoint_arn,
            MessageStructure='json',
            Message=json.dumps({
                'default': '',
                apns_key: json.dumps(apns_dict)
            })
        )

        logger.info('Sent push to {}'.format(device_id))

        return True
    except client.exceptions.EndpointDisabledException:
        logger.warn('IOS push error: Token {} is disabled'.format(device_id))

        return False


def send_silent_push_ios(device_id, data={}):
    client = create_client()

    endpoint_response = client.create_platform_endpoint(
        PlatformApplicationArn=settings.AWS_IOS_APP_ARN,
        Token=device_id
    )

    endpoint_arn = endpoint_response['EndpointArn']
    apns_key = 'APNS'
    apns_dict = {
        'aps': {
            'content-available': 1
        }
    }

    apns_dict.update(data)

    if settings.AWS_IOS_SANDBOX:
        apns_key = 'APNS_SANDBOX'
        apns_dict['aps']['sound'] = 'default'

    logger.info(apns_dict)

    try:
        client.publish(
            TargetArn=endpoint_arn,
            MessageStructure='json',
            Message=json.dumps({
                'default': '',
                apns_key: json.dumps(apns_dict)
            })
        )

        logger.info('Sent silent push to {}'.format(device_id))

        return True
    except client.exceptions.EndpointDisabledException:
        logger.warn('IOS silent push error: Token {} is disabled'.format(device_id))

        return False

