from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [ 
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', LoginView.as_view(template_name = 'login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('profiles/info/<int:user_id>/', views.profiles_info, name='profiles_info'),
    path('profiles/ban/you', views.you_is_banned, name='you_is_banned'),
    path('profiles/ban/<int:user_id>', views.ban_user, name='ban_user'),
    path('profiles/unban/<int:user_id>', views.unban_user, name='unban_user'),
    path('profiles/', views.profiles, name='profiles'),
    path('profile/', views.profile, name='profile'),
    path('profile/settings', views.profile_settings, name='profile_settings'),
    path('add_project/', views.add_project, name='add_project'),
    path('project/edit/<int:project_id>', views.edit_project, name='edit_project'),
    path('task/edit/<int:project_id>/<int:task_id>', views.edit_task, name='edit_task'),
    path('info_project/<int:project_id>/', views.info_project, name='info_project'),
    path('info_project/add_task/<int:project_id>/', views.add_task, name='add_task'),
]