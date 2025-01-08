from .forms import AddTask
from .forms import EditTask
from .forms import AddProject
from .forms import EditProject
from .forms import ProfileSettings
from .forms import ProjectFilterForm
from .forms import CustomeCreateUserForm
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.urls import reverse
from .models import Task, Project, Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return redirect('/')

def home(request):
    project = Project.objects.all()
    return render(request, "scp/home.html", {"projects":project})
def register(request):
    if request.method == 'POST':
        form = CustomeCreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CustomeCreateUserForm()
    return render(request, 'scp/register.html', {'form':form})

@login_required
def manage_particip(request, project_id):
    project = get_object_or_404(Project, id = project_id)
    return render(request, 'scp/manage_particip.html', {"project":project, "project_id":project_id})

@login_required
def you_is_banned(request):
    profile = get_object_or_404(Profile, puser = request.user)
    return render(request, 'scp/you_is_banned.html', {'profile':profile})

@login_required
def unban_user(request, user_id):
    if not request.user.profile.role == "Администратор":
        return render(request, 'scp/user_ban.html')
    user_to_ban = get_object_or_404(Profile, puser = user_id)
    user_to_ban.status = 'Не заблокирован'
    user_to_ban.save()
    return redirect('profiles')

@login_required
def ban_user(request, user_id):
    if not request.user.profile.role == "Администратор":
        return render(request, 'scp/user_ban.html')
    if request.user.id == user_id:
        return HttpResponseForbidden("Вы не можете заблокировать сами себя.")
    user_to_ban = get_object_or_404(Profile, puser = user_id)
    user_to_ban.status = 'Заблокирован'
    user_to_ban.save()
    return redirect('profiles')

@login_required
def profile_settings(request):
    profile = get_object_or_404(Profile, puser = request.user)
    if request.method == "POST":
        form = ProfileSettings(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileSettings(instance=profile)
    return render(request, 'scp/profile_settings.html', {'form':form, 'profile':profile})

@login_required
def join_task(request, task_id, project_id):
    task = get_object_or_404(Task, id = task_id)
    project = get_object_or_404(Project, id = project_id)
    if request.user != task.creator:
        if request.user != project.participants:
            task.assignee = request.user
            task.save()
        else:
            return render(request, 'scp/user_ban.html')
        return redirect('info_task', task_id = task_id, project_id = project_id)
    return render(request, 'scp/info_task.html', {'task_id':task_id, "project_id":project_id})

@login_required
def unjoin_task(request, task_id, project_id):
    task = get_object_or_404(Task, id = task_id)
    if request.user != task.creator:
        task.assignee = None
        task.save()
        return redirect('info_task', task_id = task_id, project_id = project_id)
    return render(request, 'scp/info_task.html', {'task_id':task_id, 'project_id':project_id})

@login_required
def join_project(request, project_id):
    project = get_object_or_404(Project, id = project_id)
    if request.user != project.owner:
        project.participants.add(request.user)
        project.save()
        return redirect('info_project', project_id = project.id)
    return render(request, 'scp/info_project.html', {'project_id':project_id})

@login_required
def unjoin_project(request, project_id):
    project = get_object_or_404(Project, id = project_id)
    if request.user != project.owner:
        project.participants.remove(request.user)
        project.save()
        return redirect('info_project', project_id = project.id)
    return render(request, 'scp/info_project.html', {'project_id':project_id})

@login_required
def delete_profile(request, profile_puser_id):
    if request.user.profile.role != "Администратор":
        return render(request, 'scp/user_ban.html')
    user = get_object_or_404(User, id = profile_puser_id)
    user.delete()
    return redirect('profiles')

@login_required
def delete_task(request, project_id, task_id):
    task = get_object_or_404(Task, id = task_id)
    if request.user == task.creator:
        del_task = get_object_or_404(Task, id=task_id)
        del_task.delete()  # Удаляем задачу
    else:
        return render(request,'scp/user_ban.html')   
    return redirect('info_project', project_id=project_id)  # Переходим на страницу проекта

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id = project_id)
    if request.user == project.owner:
        del_task = get_object_or_404(Project, id=project_id)
        del_task.delete()  # Удаляем проект
    else:
        return render(request,'scp/user_ban.html')    
    return redirect('profile')  # Переходим на страницу проекта

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    delete_project = reverse('delete_project', args=[project.id])
    
    # Проверяем права доступа
    if request.user == project.owner:
        if request.method == "POST":
            form = EditProject(request.POST, instance=project)
            if form.is_valid():
                form.save()
                return redirect('info_project', project_id=project.id) 
        else:
            form = EditProject(instance=project)
    else:
        # Если у пользователя нет доступа, возвращаем 403 Forbidden
        return render(request, 'scp/user_ban.html', {'project_id':project_id})

    # Гарантируем, что form всегда будет определен
    return render(request, 'scp/edit_project.html', {
        'form': form,
        'project_id': project_id,
        'project': project,
        'delete_project': delete_project
    })

@login_required
def edit_task(request, task_id, project_id):
    task = get_object_or_404(Task, id = task_id)
    project = get_object_or_404(Project, id = project_id)  # Исправлено: использую project_id для поиска проекта
    delete_task = reverse('delete_task', args=[task.id, project.id])
    if request.method == "POST":
        form = EditTask(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('info_task', task_id=task_id,project_id=project_id )  # Исправлено: правильный редирект
    else:
        form = EditTask(instance=task)

    return render(request, 'scp/edit_task.html', {
        'form': form, 
        'project_id': project_id, 
        'task_id': task_id, 
        'task': task,
        'delete_task': delete_task  # Передаем URL для удаления задачи
    })

@login_required
def info_project(request, project_id):
    project = get_object_or_404(Project, id = project_id)
    profile = Profile.objects.select_related('profile')
    is_participant = project.participants.filter(id=request.user.id).exists()
    tasks = Task.objects.filter(project = project_id)

    context = {
        'project':project,
        'is_participant':is_participant,
        'tasks':tasks,
        'profile':profile,

    }

    return render(request, 'scp/info_project.html', context)

@login_required
def info_task(request, task_id, project_id):
    project = get_object_or_404(Project, id = project_id)
    task = get_object_or_404(Task, id = task_id)
    is_assignee = task.assignee is not None
    context = {
        'is_assignee':is_assignee,
        'task':task,
        'task_id': task.id,
        'project_id': project.id
    }

    return render(request, 'scp/info_task.html', context)

@login_required
def profile(request):
    profiles = get_object_or_404(Profile, puser = request.user)
    projects = Project.objects.filter(owner = request.user)
    memberprojects = Project.objects.filter(participants = request.user)
    return render(request, 'scp/profile.html', {'profile':profiles, 'projects':projects, "memberprojects":memberprojects})

@login_required
def profiles(request):
    users = User.objects.all()
    return render(request, 'scp/profiles.html', {'users':users})

@login_required
def profiles_info(request, user_id):
    profiles = get_object_or_404(Profile, puser = user_id)
    projects = Project.objects.filter(owner = user_id)
    return render(request, 'scp/profiles_info.html', {'profile':profiles, 'projects':projects})

@login_required
def admin_panel(request, user_id):
    profiles = get_object_or_404(Profile, puser = user_id)
    projects = Project.objects.filter(owner = user_id)
    return render(request, 'scp/admin_panel.html', {'profile':profiles, 'projects':projects})

@login_required
def add_project(request):
    if request.method == "POST":
        form = AddProject(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('profile')
    else:
        form = AddProject()
    return render(request,'scp/add_project.html', {'form':form})

@login_required
def add_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)  # Изменено на Project
    if request.method == "POST":
        form = AddTask(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user  # Привязка создателя
            task.project = project       # Привязка проекта
            task.save()
            return redirect('info_project', project_id=project.id)
    else:
        form = AddTask()
    return render(request, 'scp/add_task.html', {'form': form})