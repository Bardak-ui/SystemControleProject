from django.contrib import admin
from .models import Task, Profile, Project, Post, Comment

admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)