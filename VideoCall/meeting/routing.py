from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('meeting/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]