from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models as m
from . import serializers as s
from .pagination import DateUpdatedPagination, DateCreatedPagination


class DiscussionTopicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = m.DiscussionTopic.objects.all()
    serializer_class = s.DiscussionTopicSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = DateUpdatedPagination

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class InitiativeViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = m.Initiative.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'feedback':
            return s.InitiativeFeedbackSerializer

        return s.InitiativeSerializer

    @action(detail=True, methods=['PUT'])
    def feedback(self, request, pk=None):
        initiative = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(initiative=initiative, user=self.request.user)

        return Response(serializer.data)

    @action(detail=True, methods=['POST'], )
    def add_step(self, request, pk=None):
        return Response('')


class AnnouncementViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = m.Announcement.objects.all()
    serializer_class = s.AnnouncementSerializer
    permission_classes = (IsAuthenticated, )


class InitiativeProcessStepViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = m.InitiativeProcessStep
    serializer_class = s.InitiativeProcessStepSerializer
    permission_classes = (IsAuthenticated, )


class AdvertisementCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = m.AdvertisementCategory.objects.all()
    serializer_class = s.AdvertisementCategorySerializer
    permission_classes = (IsAuthenticated, )
    ordering = ('order_col', )


class AdvertisementViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = s.AdvertisementSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = DateCreatedPagination

    def get_queryset(self):
        queryset = m.Advertisement.objects.all()

        if 'subcategory' in self.request.query_params:
            queryset = queryset.filter(subcategory=self.request.query_params['subcategory'])

        return queryset
