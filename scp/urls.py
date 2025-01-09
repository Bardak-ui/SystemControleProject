from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [ 
    path('logout/', views.logout_view, name='logout_view'), # Страница выхода
    path('login/', LoginView.as_view(template_name = 'scp/login.html'), name='login'), # Страница входа
    path('register/', views.register, name='register'), # Страница регистрации
    path('home/', views.home, name='home'), # Домашняя страница (страница со всеми проектами)
    path('forum/', views.forum, name='forum'), # Форум (страница с постами пользователей)
    # работа с профилями других пользователей
    path('profiles/info/<int:user_id>/', views.profiles_info, name='profiles_info'), 
    path('profiles/ban/you', views.you_is_banned, name='you_is_banned'),
    path('profiles/ban/<int:user_id>', views.ban_user, name='ban_user'),
    path('profiles/delete_user/<int:profile_puser_id>', views.delete_profile, name='delete_profile'),
    path('profiles/unban/<int:user_id>', views.unban_user, name='unban_user'),
    path('profiles/', views.profiles, name='profiles'),
    # -----------------------------------------------------------------------
    path('profile/', views.profile, name='profile'), # Профиль
    path('admin-panel/<int:user_id>', views.admin_panel, name='admin_panel'), # Панель администратора
    path('profile/settings', views.profile_settings, name='profile_settings'), # Настройки профиля
    path('project/edit/<int:project_id>/', views.edit_project, name='edit_project'), # Изменение проекта
    # -----------------------------------------------------------------------
    path('add_project/', views.add_project, name='add_project'), # Добавление проекта
    path('task/delete/<int:task_id>/<int:project_id>/', views.delete_task, name='delete_task'), # Изменение задачи
    path('project/delete/<int:project_id>/', views.delete_project, name='delete_project'), # Изменение задачи
    path('task/edit/<int:task_id>/<int:project_id>/', views.edit_task, name='edit_task'), # Изменение задачи
    path('info_project/<int:project_id>/', views.info_project, name='info_project'), # Информация о проекте
    path('info_project/add_task/<int:project_id>/', views.add_task, name='add_task'), # Добавление задачи к проекту
    path('info_project/join_project/<int:project_id>/', views.join_project, name='join_project'), 
    path('info_project/unjoin_project/<int:project_id>/', views.unjoin_project, name='unjoin_project'), 
    path('info_project/manage_particip/<int:project_id>/', views.manage_particip, name='manage_particip'), 
    path('info_task/<int:task_id>/<int:project_id>/', views.info_task, name='info_task'), 
    path('info_task/join_task/<int:task_id>/<int:project_id>/', views.join_task, name='join_task'), 
    path('info_task/unjoin_task/<int:task_id>/<int:project_id>/', views.unjoin_task, name='unjoin_task'), 
    #path('manage_particip/delete/<int:user_id>/')
]