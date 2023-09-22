from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from baladiya.consumers import *

websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<first_user_id>\w+)/(?P<second_user_id>\w+)/",
        ChatConsumer.as_asgi(),
    ),
]
