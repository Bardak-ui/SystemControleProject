from django.shortcuts import redirect
from django.urls import reverse

class BanCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверка на авторизованного пользователя
        if request.user.is_authenticated:
            # Проверяем наличие профиля и статус
            profile = getattr(request.user, 'profile', None)
            if profile and profile.status == 'Заблокирован':  # Здесь ваш статус "Заблокирован"
                # Перенаправляем на страницу бана
                return redirect(reverse('you_is_banned'))  # Убедитесь, что путь 'banned_page' существует
        return self.get_response(request)
