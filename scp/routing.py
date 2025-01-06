#routing.py
from django.urls import path
from .consumers import OnlineStatusConsumer  # Импортируем ваш Consumer

# Настроим маршруты для WebSocket
websocket_urlpatterns = [
    path('ws/online_status/', OnlineStatusConsumer.as_asgi()),  # Путь для WebSocket
]

# from django.urls import path
# from .consumers import OnlineStatusConsumer

# websocket_urlpatterns = [
#     path('ws/online_status/', OnlineStatusConsumer.as_asgi()),  # Правильный путь
# ]
