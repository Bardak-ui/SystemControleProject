from .forms import AddTask
from .forms import EditTask
from .forms import AddProject
from .forms import EditProject
from .forms import ProfileSettings
from .forms import ProjectFilterForm
from .forms import CustomeCreateUserForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from .models import Task, Project, Profile

def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

def you_is_banned(request):
    return render(request, 'you_is_banned.html')

def unban_user(request, user_id):
    if not request.user.profile.role == "Администратор":
        return render(request, 'user_ban.html')
    user_to_ban = get_object_or_404(Profile, puser = user_id)
    user_to_ban.status = 'Не заблокирован'
    user_to_ban.save()
    return redirect('profiles')

@login_required
def ban_user(request, user_id):
    if not request.user.profile.role == "Администратор":
        return render(request, 'user_ban.html')
    if request.user.id == user_id:
        return HttpResponseForbidden("Вы не можете заблокировать сами себя.")
    user_to_ban = get_object_or_404(Profile, puser = user_id)
    user_to_ban.status = 'Заблокирован'
    user_to_ban.save()
    return redirect('profiles')


@login_required
def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html', {'projects':projects})

def register(request):
    if request.method == 'POST':
        form = CustomeCreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CustomeCreateUserForm()
    return render(request, 'register.html', {'form':form})

@login_required
def profile_settings(request):
    profile = get_object_or_404(Profile, puser = request.user)
    if request.method == "POST":
        form = ProfileSettings(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileSettings(instance=request.user.profile)
    return render(request, 'profile_settings.html', {'form':form, 'profile':profile})


@login_required
def join_task(request):
    pass

@login_required
def join_project(request):
    pass

@login_required
def edit_project(request, project_id):
        project = get_object_or_404(Project, id = project_id)
        if request.user == project.participants:
            if request.method == "POST":
                form = EditProject(request.POST, instance=project)
                if form.is_valid():
                    form.save()
                    return redirect('info_project', project_id=project.id)
            else:
                form = EditProject(instance=project)
            return render(request,'edit_project.html',{'form':form, 'project':project, 'project_id':project_id})
        return HttpResponseForbidden("Вы не учавствуете в разработке этого проекта.")

@login_required
def delete_task(request, project_id, task_id):
    del_task = get_object_or_404(Task, id=task_id)
    del_task.delete()  # Удаляем задачу
    # Нет необходимости вызывать save(), так как объект уже удален

    return redirect('info_project', project_id=project_id)  # Переходим на страницу проекта



@login_required
def edit_task(request, project_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = get_object_or_404(Project, id=project_id)  # Исправлено: использую project_id для поиска проекта
    delete_url = reverse('delete_task', args=[task.id, project.id])
    
    if request.method == "POST":
        form = EditTask(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('info_project', project_id=project_id)  # Исправлено: правильный редирект
    else:
        form = EditTask(instance=task)
    
    return render(request, 'edit_task.html', {
        'form': form, 
        'project_id': project_id, 
        'task_id': task_id, 
        'task': task,
        'delete_url': delete_url  # Передаем URL для удаления задачи
    })

@login_required
def info_project(request, project_id):
    project = get_object_or_404(Project, id = project_id)
    tasks = Task.objects.filter(project = project_id)
    return render(request, 'info_project.html', {'project':project, 'tasks':tasks})

@login_required
def profile(request):
    profiles = get_object_or_404(Profile, puser = request.user)
    projects = Project.objects.filter(owner = request.user)
    return render(request, 'profile.html', {'profile':profiles, 'projects':projects})

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
    return render(request,'add_project.html', {'form':form})

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
    return render(request, 'add_task.html', {'form': form})

def profiles(request):
    users = User.objects.all()
    return render(request, 'profiles.html', {'users':users})

def profiles_info(request, user_id):
    profiles = get_object_or_404(Profile, puser = user_id)
    projects = Project.objects.filter(owner = user_id)
    return render(request, 'profiles_info.html', {'profile':profiles, 'projects':projects})    