from rest_framework import routers

from accounts.router import register as register_accounts
from chats.router import register as register_chats
from notifications.router import register as register_notifications
from democracy.router import register as register_democracy

router = routers.DefaultRouter()

register_accounts(router)
register_chats(router)
register_notifications(router)
register_democracy(router)
