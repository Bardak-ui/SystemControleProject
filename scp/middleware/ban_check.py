from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout

class BanCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Если запрос касается выхода, пропускаем обработку блокировки
        if request.path == reverse('logout_view'):  # Замените 'logout' на имя вашего URL для выхода
            return self.get_response(request)
        
        # Проверяем, если пользователь авторизован
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            # Если у пользователя есть профиль и статус "Заблокирован"
            if profile and profile.status == 'Заблокирован':
                # Если пользователь заблокирован, перенаправляем на страницу с сообщением
                return render(request, 'you_is_banned.html')

        # Если пользователь не заблокирован, продолжаем обработку запроса
        response = self.get_response(request)
        return response
