import requests
from django.db.models import Max
from django.conf import settings
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models as m
from . import serializers as s
from .pagination import DateCreatedPagination


class ChatViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = m.Chat.objects.all()
        queryset = queryset.annotate(last_message_created=Max('messages__date_created'))

        return queryset.order_by('last_message_created')

    def get_serializer_class(self):
        if self.action in ['messages']:
            return s.MessageSerializer

        return s.ChatSerializer

    @action(detail=True, methods=['GET'], pagination_class=DateCreatedPagination)
    def messages(self, request, pk=None):
        chat = self.get_object()

        queryset = chat.messages.all().order_by('-date_created')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MessageViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = s.MessageSerializer

    def get_queryset(self):
        user = self.request.user

        if not user or not user.pk:
            return m.Message.objects.none()

        return m.Message.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        requests.post(settings.WEBSOCKET_API_ENDPOINT, json=serializer.data)
