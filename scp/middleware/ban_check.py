from django.shortcuts import redirect

class BanCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile') and request.user.profile.status == 'Baned':
                return redirect('you_is_banned')  # Перенаправление на страницу бана
        return self.get_response(request)
