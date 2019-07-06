# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models as m


class UserDeviceSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = m.UserDevice
        fields = ('id', 'user', 'device_type', 'device_id', )

    def validate(self, data):
        data = super().validate(data)

        try:
            m.UserDevice.objects.get(
                user=data['user'],
                device_type=data['device_type'],
                device_id=data['device_id']
            )
            raise ValidationError({'detail': 'User already has bound this device.', 'status': 2002})
        except m.UserDevice.DoesNotExist:
            pass

        return data
