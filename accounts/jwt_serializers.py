from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username_field, PasswordField, Serializer
import rest_framework_jwt.utils as jwt_utils


User = get_user_model()
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class JSONWebTokenSerializer(Serializer):
    """
    Serializer class used to validate a username and password.
    'username' is identified by the custom UserModel.USERNAME_FIELD.
    Returns a JSON Web Token that can be used to authenticate later calls.
    """
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        username_val = attrs.get(self.username_field).lower()
        user = User.objects.get_by_natural_key(username_val)

        if user:
            username_val = user.username
        else:
            username_val = f'email::{username_val}'

        credentials = {
            self.username_field: username_val,
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                # if user.confirmation_code:
                #     account_type = 'email'
                #     account_val = user.email
                #
                #     msg = {
                #         'non_field_errors': [
                #             _('User must confirm {account_type}.').format(account_type=account_type)
                #         ],
                #         'status': 1001,
                #         'account_type': account_type,
                #         account_type: account_val
                #     }
                #
                #     raise serializers.ValidationError(msg)

                user.last_login = timezone.now()
                user.save()

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


def jwt_payload_handler(user):
    payload = jwt_utils.jwt_payload_handler(user)

    if user.is_authenticated:
        payload['expRemaining'] = int((payload.get('exp') - datetime.utcnow()).total_seconds())
        payload['expDelta'] = int(api_settings.JWT_EXPIRATION_DELTA.total_seconds())

    return payload


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
