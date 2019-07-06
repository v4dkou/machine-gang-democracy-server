from rest_framework import serializers

from . import models as m
from accounts.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = m.Message
        fields = (
            'id',
            'user',
            'chat',
            'text',
        )
