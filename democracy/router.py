from . import viewsets as v

def register(router):
    router.register('discussion_topics', v.DiscussionTopicViewSet, base_name='discussion_topics')
    router.register('announcements', v.AnnouncementViewSet, base_name='announcements')
    router.register('initiatives', v.InitiativeViewSet, base_name='initiatives')
