from rest_framework import serializers

from . import models as m


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = m.User
        fields = (
            'id',
            'username',
            'fullname',
            'avatar',
        )
