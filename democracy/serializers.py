from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers

from accounts.serializers import UserSerializer
from chats.models import Chat
from . import models as m


class DiscussionTopicSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = m.DiscussionTopic
        fields = (
            'id',
            'user',
            'chat',
            'description',
            'image',
            'alert',
            'status',
            'initiative',
            'announcement',
            'date_created',
            'date_updated',
        )
        read_only_fields = (
            'id',
            'user',
            'chat',
            'alert',
            'status',
            'initiative',
            'announcement',
            'date_created',
            'date_updated',
        )

    def create(self, data):
        # Create chat and set user
        chat = Chat.objects.create()

        data['chat'] = chat
        data['user'] = self.context.get('request').user

        return super().create(data)


class InitiativeProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.InitiativeProcessStep
        fields = (
            'order_col',
            'name',
            'status',
        )


class InitiativeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.InitiativeFeedback
        fields = (
            'relevance',
            'vote',
        )


class InitiativeSerializer(serializers.ModelSerializer):
    topic = DiscussionTopicSerializer(read_only=True)
    feedback = serializers.SerializerMethodField()
    steps = InitiativeProcessStepSerializer(many=True, read_only=True)

    votes = serializers.SerializerMethodField()
    relevance = serializers.SerializerMethodField()

    class Meta:
        model = m.Initiative
        fields = (
            'topic',
            'problem_description',
            'solution_description',
            'feedback',
            'steps',
            'votes',
            'relevance',
        )

    def get_feedback(self, obj):
        user = self.context.get('request').user

        if not user or not user.pk:
            return None

        try:
            feedback = obj.feedbacks.get(user=user)
        except m.InitiativeFeedback.DoesNotExist:
            feedback = m.InitiativeFeedback()

        return InitiativeFeedbackSerializer(feedback).data

    def create(self, data):
        # Validate and create DiscussionTopic
        if 'topic' not in self.initial_data:
            raise serializers.ValidationError({'topic': 'Topic is required field.'})

        topic = self.initial_data.pop('topic')
        topic_serializer = DiscussionTopicSerializer(data=topic, context=self.context)
        topic_serializer.is_valid(raise_exception=True)
        topic_serializer.save()

        data['topic'] = topic_serializer.instance

        initiative = super().create(data)

        m.InitiativeProcessStep.objects.create(
            initiative=initiative,
            order_col=1,
            name='Обсуждение'
        )

        m.InitiativeProcessStep.objects.create(
            initiative=initiative,
            order_col=2,
            name='Голосование'
        )

        return initiative

    def get_votes(self, obj):
        return {
            'yes': obj.feedbacks.filter(vote=True).count(),
            'no': obj.feedbacks.filter(vote=False).count(),
        }

    def get_relevance(self, obj):
        return {
            'num_votes': obj.feedbacks
                .filter(relevance__isnull=False)
                .count(),

            'sum_relevance': obj.feedbacks
                .filter(relevance__isnull=False)
                .aggregate(sum_relevance=Coalesce(Sum('relevance'), 0))
                .get('sum_relevance')
        }


class AnnouncementSerializer(serializers.ModelSerializer):
    topic = DiscussionTopicSerializer(read_only=True)

    class Meta:
        model = m.Announcement
        fields = (
            'topic',
            'announcement_description',
        )

    def create(self, data):
        # Validate and create DiscussionTopic
        if 'topic' not in self.initial_data:
            raise serializers.ValidationError({'topic': 'Topic is required field.'})

        topic = self.initial_data.pop('topic')
        topic_serializer = DiscussionTopicSerializer(data=topic, context=self.context)
        topic_serializer.is_valid(raise_exception=True)
        topic_serializer.save()

        data['topic'] = topic_serializer.instance

        return super().create(data)


class AdvertisementSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.AdvertisementSubcategory
        fields = ('id', 'name', )
        read_only_fields = ('id', 'name', )


class AdvertisementCategorySerializer(serializers.ModelSerializer):
    subcategories = AdvertisementSubcategorySerializer(many=True, read_only=True)
    promo = serializers.SerializerMethodField()

    class Meta:
        model = m.AdvertisementCategory
        fields = (
            'id',
            'name',
            'subcategories',
            'promo',
        )
        read_only_fields = (
            'id',
            'name',
            'subcategories',
            'promo',
        )

    def get_promo(self, obj):
        promo = m.Advertisement.objects \
            .filter(subcategory__category=obj, is_paid=True) \
            .order_by('?') \
            .first()

        if not promo:
            return None

        return AdvertisementSerializer(promo).data


class AdvertisementSerializer(serializers.ModelSerializer):
    subcategory = AdvertisementSubcategorySerializer()

    class Meta:
        model = m.Advertisement
        fields = (
            'id',
            'subcategory',
            'title',
            'description',
            'image',
            'price',
            'range',
            'is_paid',
            'paid_period',
        )
