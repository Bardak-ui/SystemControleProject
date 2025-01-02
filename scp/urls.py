from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [ 
    path('logout/', views.logout_view, name='logout_view'), # Страница выхода
    path('login/', LoginView.as_view(template_name = 'login.html'), name='login'), # Страница входа
    path('register/', views.register, name='register'), # Страница регистрации
    path('home/', views.home, name='home'), # Домашняя страница (страница со всеми проектами)
    # работа с профилями других пользователей
    path('profiles/info/<int:user_id>/', views.profiles_info, name='profiles_info'), 
    path('profiles/ban/you', views.you_is_banned, name='you_is_banned'),
    path('profiles/ban/<int:user_id>', views.ban_user, name='ban_user'),
    path('profiles/unban/<int:user_id>', views.unban_user, name='unban_user'),
    path('profiles/', views.profiles, name='profiles'),
    # ----------------
    path('profile/', views.profile, name='profile'), # Профиль
    path('profile/settings', views.profile_settings, name='profile_settings'), # Настройки профиля
    path('project/edit/<int:project_id>/', views.edit_project, name='edit_project'), # Изменение проекта
    # -----------------
    path('add_project/', views.add_project, name='add_project'), # Добавление проекта
    path('task/delete/<int:task_id>/<int:project_id>/', views.delete_task, name='delete_task'), # Изменение задачи
    path('task/edit/<int:project_id>/<int:task_id>/', views.edit_task, name='edit_task'), # Изменение задачи
    path('info_project/<int:project_id>/', views.info_project, name='info_project'), # Информация о проекте
    path('info_project/add_task/<int:project_id>/', views.add_task, name='add_task'), # Добавление задачи к проекту
]