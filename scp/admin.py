from django.contrib import admin
from .models import Task, Profile, Project

admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Profile)