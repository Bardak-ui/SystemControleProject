from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from scp.models import Profile

class BanCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Если запрос касается выхода, пропускаем обработку блокировки
        if request.path == reverse('logout_view'):  # Убедитесь, что 'logout' соответствует вашему URL для выхода
            return self.get_response(request)

        # Проверяем, если пользователь авторизован
        if request.user.is_authenticated:
            #profile = getattr(request.user, 'profile', None)
            profile = get_object_or_404(Profile, puser = request.user)
            # Если у пользователя есть профиль и статус "Заблокирован"
            if profile and profile.status == 'Заблокирован':
                # Если пользователь заблокирован, передаем данные профиля в шаблон блокировки
                return render(request, 'scp/you_is_banned.html', {'profile': profile})

        # Если пользователь не заблокирован, продолжаем обработку запроса
        response = self.get_response(request)
        return response
