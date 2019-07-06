from . import viewsets as v

def register(router):
    router.register('chats', v.ChatViewSet, base_name='chats')
    router.register('messages', v.MessageViewSet, base_name='messages')
