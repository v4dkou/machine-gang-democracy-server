from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models

from accounts.models import User
from chats.models import Chat


class DiscussionTopic(models.Model):
    NEW = 'new'
    VOTING = 'voting'
    CLOSED = 'closed'

    STATUSES = (
        (NEW, 'New'),
        (VOTING, 'Voting'),
        (CLOSED, 'Closed'),
    )

    user = models.ForeignKey(User, verbose_name='Owner', related_name='discussion_topics', on_delete=models.CASCADE)
    description = models.TextField('Description')
    image = models.ImageField(upload_to='discussion_images', null=True, blank=True)
    status = models.CharField('Status', max_length=16, choices=STATUSES, default=NEW)
    chat = models.ForeignKey(Chat, related_name='topic', on_delete=models.CASCADE)
    alert = models.BooleanField('Is alert', default=False)

    date_created = models.DateTimeField('Created', default=timezone.now, editable=False)
    date_updated = models.DateTimeField('Updated', auto_now=True)


class Initiative(models.Model):
    topic = models.OneToOneField(DiscussionTopic, verbose_name='Topic', primary_key=True, on_delete=models.CASCADE, related_name='initiative')

    problem_description = models.TextField('Problem description')
    solution_description = models.TextField('Solution description')


class InitiativeProcessStep(models.Model):
    NEW = 'new'
    COMPLETE = 'complete'

    STATUSES = (
        (NEW, 'New'),
        (COMPLETE, 'Complete'),
    )

    initiative = models.ForeignKey(Initiative, verbose_name='Initiative', related_name='steps', on_delete=models.CASCADE)
    order_col = models.PositiveIntegerField('Order', default=1)

    status = models.CharField('Status', max_length=16, choices=STATUSES, default=NEW)
    name = models.CharField('Step name', max_length=255)

    date_created = models.DateTimeField('Created', default=timezone.now, editable=False)
    date_updated = models.DateTimeField('Updated', auto_now=True)


class InitiativeFeedback(models.Model):
    user = models.ForeignKey(User, verbose_name='Owner', related_name='initiative_feedbacks', on_delete=models.CASCADE)
    initiative = models.ForeignKey(Initiative, verbose_name='Initiative', related_name='feedbacks', on_delete=models.CASCADE)

    relevance = models.PositiveIntegerField('Relevance', default=3)
    vote = models.NullBooleanField('Vote', default=None)

    class Meta:
        unique_together = ('user', 'initiative', )


class Announcement(models.Model):
    topic = models.OneToOneField(DiscussionTopic, verbose_name='Topic', primary_key=True, on_delete=models.CASCADE, related_name='announcement')

    announcement_description = models.TextField('Announcement description')


class AdvertisementCategory(models.Model):
    name = models.CharField('Name', max_length=255)

    order_col = models.PositiveIntegerField('Order', default=0)


class AdvertisementSubcategory(models.Model):
    category = models.ForeignKey(AdvertisementCategory, verbose_name='Category', related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=255)

    order_col = models.PositiveIntegerField('Order', default=0)


class Advertisement(models.Model):
    subcategory = models.ForeignKey(AdvertisementSubcategory, verbose_name='Subcategory', related_name='ads', on_delete=models.CASCADE)

    title = models.CharField('Title', max_length=255)
    description = models.TextField('Description')
    image = models.ImageField(upload_to='ads_images')

    price = models.PositiveIntegerField('Price', default=0)
    range = models.PositiveIntegerField('Range', default=0)

    is_paid = models.BooleanField('Is paid')
    paid_period = models.PositiveIntegerField('Paid period', default=0)

    date_created = models.DateTimeField('Created', default=timezone.now, editable=False)
