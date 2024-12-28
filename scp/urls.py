from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [ 
    path('', LoginView.as_view(template_name = 'login.html'), name='login'),
    path('login/', LoginView.as_view(template_name = 'login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('add_project/', views.add_project, name='edit_project'),
]