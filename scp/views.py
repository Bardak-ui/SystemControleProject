from .forms import CustomeCreateUserForm, AddProject, ProfileSettings, ProjectFilterForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Task, Project, Profile

def home(request):
    projects = Project.objects.all()
    #домашняя страница вывод всех проектов на сайте
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

# def edit_project(request, task_id):

def profile_settings(request):
    if request.method == "POST":
        form = ProfileSettings(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileSettings(instance=request.user.profile)
    return render(request, 'profile_settings.html', {'form':form})

def profile(request):
    profile = get_object_or_404(Profile, user = request.user.profile)
    return render(request, 'profile.html', {'profile':profile})

def add_project(request):
    if request.method == "POST":
        form = AddProject(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddProject()
    return render(request,'add_project.html', {'form':form})

#profile, profile_settings, add_project, add_task, admin_panel,


