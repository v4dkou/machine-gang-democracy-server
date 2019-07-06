from django.contrib import admin

from democracy import models as m


class InitiativeFeedbackInline(admin.TabularInline):
    model = m.InitiativeFeedback
    extra = 1


class InitiativeProcessStepInline(admin.TabularInline):
    model = m.InitiativeProcessStep
    extra = 1


class InitiativeInline(admin.StackedInline):
    model = m.Initiative
    extra = 0


class AnnouncementInline(admin.StackedInline):
    model = m.Announcement
    extra = 0


@admin.register(m.DiscussionTopic)
class DiscussionTopicAdmin(admin.ModelAdmin):
    inlines = (InitiativeInline, AnnouncementInline, )
