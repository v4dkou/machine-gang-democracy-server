from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models

from accounts.models import User
from chats.models import Chat


class DiscussionTopic(models.Model):
    NEW = 'new'
    CLOSED = 'closed'
    STATUSES = (
        (NEW, 'New'),
        (CLOSED, 'Closed'),
    )

    user = models.ForeignKey(User, verbose_name='Owner', related_name='discussion_topics', on_delete=models.CASCADE)
    description = models.TextField('Description')
    status = models.CharField('Status', max_length=16, choices=STATUSES, default=NEW)
    chat = models.ForeignKey(Chat, related_name='topic', on_delete=models.CASCADE)

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
