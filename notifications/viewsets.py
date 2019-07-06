# -*- coding: utf-8 -*-
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from . import models as m
from . import serializers as s


class UserDeviceViewSet(CreateModelMixin, DestroyModelMixin, ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return m.UserDevice.objects \
            .filter(user=self.request.user) \
            .order_by('-date_created')

    def get_serializer_class(self):
        return s.UserDeviceSerializer
