import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Profile

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Получаем пользователя из scope (если он аутентифицирован)
        self.user = self.scope['user']
        
        # Если пользователь не аутентифицирован, отклоняем подключение
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Получаем профиль пользователя
        self.profile = await sync_to_async(Profile.objects.get)(puser=self.user)

        # Устанавливаем аккаунт в True (онлайн)
        await self.set_online_status(True)

        # Подключаем WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # При отключении устанавливаем аккаунт в False (офлайн)
        await self.set_online_status(False)

        # Закрываем соединение
        await self.close()

    async def set_online_status(self, status):
        # Обновляем поле account в базе данных
        await sync_to_async(self.update_status)(status)

        # Отправляем обновленный статус всем подключенным клиентам
        await self.send(text_data=json.dumps({
            'status': 'online' if status else 'offline'
        }))

    def update_status(self, status):
        # Обновляем поле account
        self.profile.account = status
        self.profile.save()
