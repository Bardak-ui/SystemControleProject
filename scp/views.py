from .forms import CustomeCreateUserForm, AddProject, ProfileSettings, ProjectFilterForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Task, Project, Profile

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html', {'projects':projects})

def register(request):
    if request.method == 'POST':
        form = CustomeCreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomeCreateUserForm()
    return render(request, 'register.html', {'form':form})

@login_required
def edit_project(request, task_id):
    pass

@login_required
def info_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id = project_id)
        task = Task.objects.filter(project)
    return render(request, 'info_project.html', {'projects':project, 'task':task})

@login_required
def profile_settings(request):
    if request.method == "POST":
        form = ProfileSettings(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileSettings(instance=request.user.profile)
    return render(request, 'profile_settings.html', {'form':form})

@login_required
def profile(request):
    profiles = get_object_or_404(Profile, user = request.user)
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

#profile, profile_settings, add_project, add_task, admin_panel,
#сделать функцию для вступления в проект и вступление в разруботку задачи для проекта

