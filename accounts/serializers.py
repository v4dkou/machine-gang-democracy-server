from rest_framework import serializers

from . import models as m


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.User
        fields = (
            'id',
            'username',
        )
