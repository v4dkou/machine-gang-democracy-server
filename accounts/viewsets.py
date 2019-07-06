from rest_framework import viewsets
from rest_framework import mixins

from . import models as m
from . import serializers as s


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = m.User
    serializer_class = s.UserSerializer
