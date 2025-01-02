# routing.py
from django.urls import path
from .consumers import OnlineStatusConsumer  # Импортируйте ваш Consumer

websocket_urlpatterns = [
    path('ws/online_status/', OnlineStatusConsumer.as_asgi()),
]
