# asgi.py
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemControleProject.settings')

# Важное изменение: вызываем django.setup() ДО импорта
django.setup()

# Теперь можно импортировать все нужные компоненты
from scp.routing import websocket_urlpatterns

# Применяем настройку протоколов для WebSocket и HTTP
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Обработка HTTP-запросов
    "websocket": AuthMiddlewareStack(  # Для WebSocket добавляем авторизацию
        URLRouter(websocket_urlpatterns)  # Подключаем маршруты WebSocket
    ),
})


# import os
# import django
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemControleProject.settings')

# django.setup()

# from scp.routing import websocket_urlpatterns

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(websocket_urlpatterns)
#     ),
# })
