from rest_framework import routers

from accounts.router import register as register_accounts
from chats.router import register as register_chats

router = routers.DefaultRouter()

register_accounts(router)
register_chats(router)
