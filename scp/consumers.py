#consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Profile, Comment, Post
from django.contrib.auth.models import User

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            # Обновляем статус онлайн
            await self.set_online_status(True)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Обновляем статус оффлайн
            await self.set_online_status(False)

    @sync_to_async  # Делаем это синхронной функцией для работы с ORM
    def set_online_status(self, status):
        try:
            # Используем puser для поиска профиля
            profile = Profile.objects.get(puser=self.user)
            profile.account = status  # Обновляем поле account
            profile.save()  # Сохраняем изменения
        except Profile.DoesNotExist:
            pass

    async def receive(self, text_data):
        # Обработка входящих сообщений
        await self.send(text_data=json.dumps({
            'message': 'Сообщение получено!'
        }))