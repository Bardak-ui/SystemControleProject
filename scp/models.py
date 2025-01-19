import os
from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    ROLE_CHOICES = [
        ('Администратор','Administrator'),
        ('Исполнитель','Executor'),
    ]


class Language(models.Model):
    LANGUAGE_CHOICES = [
        ('C', 'С'),
        ('C++', 'С++'),
        ('C#', 'С#'),
        ('Go', 'Go'),
        ('Java', 'Java'),
        ('JavaScript', 'JavaScript'),
        ('Kotlin', 'Kotlin'),
        ('PHP', 'PHP'),
        ('Python', 'Python'),
        ('Ruby', 'Ruby'),
        ('Rust', 'Rust'),
        ('TypeScript', 'TypeScript'),
        ('Swift', 'Swift'),
        ('Shell', 'Shell'),
        ('Perl', 'Perl'),
        ('Lua', 'Lua'),
        ('SQL', 'SQL'),
        ('Assembly', 'Ассемблер'),
        ('Не указан', 'Не указан'),
    ]

class Status(models.Model):
    STATUS_CHOICES = [('Выполнено','Выполнено'),
                      ('В разработке','В разработке'),
                      ('Ожидает','Ожидает')
                      ]
    
    PRIORITY_CHOICES = [('Низкий','Низкий'),
                        ('Cредний','Cредний'),
                        ('Высокий','Высокий'),
                        ('Не указан','Не указан')
                        ]
    
    BLACKLIST_CHOICES = [('Заблокирован','Заблокирован'),
                         ('Не заблокирован','Не заблокирован'),
                         ]
    ACCSTATUS_CHOICES_CHOICES = [
        ('Онлайн','Online'),
        ('Офлайн','Оffline'),
        ('Деактивирована','Deactivated')
    ]

class Post(models.Model):
    title = models.CharField(max_length=100)
    anons = models.CharField(max_length=250, verbose_name='Краткое описание поста')
    text = models.TextField()
    creator = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statia_user')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.creator} on {self.created_at}"
    
class Comment(models.Model):
    message = models.CharField(max_length=3000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='message_user')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.created_at}"

class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название проекта')
    description = models.TextField(verbose_name='Описание проекта')
    # tasks = models.ManyToManyField(Task, related_name='p_tasks')
    code = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, choices=Language.LANGUAGE_CHOICES, verbose_name='Язык программирования',default='Не указан')
    status = models.CharField(max_length=50,choices=Status.STATUS_CHOICES, verbose_name="Статус",default='Ожидает')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='p_owner')
    participants = models.ManyToManyField(User, blank=True, related_name='p_participants')
    created_at = models.DateField(auto_now_add=True)
    complexity = models.OneToOneField(Status, choices=Status.STATUS_CHOICES, verbose_name="Сложность", on_delete=models.CASCADE,default='Не указан',related_name='p_complexity')
    # updated_at = models.DateField() #Реализовать дату последнего обновления

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=100, null=False, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='t_creator')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='t_project')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, blank = True,null=True,related_name='t_assignee')
    priority = models.CharField(max_length=50, choices=Status.PRIORITY_CHOICES,verbose_name="Статус",default='Не указан')
    status = models.CharField(max_length=50,choices=Status.STATUS_CHOICES, verbose_name="Cтатус",default='Ожидает')
    created_at = models.DateField(auto_now_add=True)
    # updated_at = models.DateField() #Реализовать дату последнего обновления

    def __str__(self):
        return self.title

class Profile(models.Model):
    puser = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='./profile_avatars/', blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, choices=Role.ROLE_CHOICES, default='Исполнитель')
    account = models.BooleanField(default=False)  # Это поле отвечает за статус пользователя
    status = models.CharField(max_length=50, choices=Status.BLACKLIST_CHOICES, default='Не заблокирован')
    def __str__(self):
        return f"{self.puser}'s Profile"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_avatar = Profile.objects.get(pk = self.pk).avatar
            if old_avatar and old_avatar != self.avatar:
                if os.path.isfile(old_avatar.path):
                    os.remove(old_avatar.path)
        super(Profile, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
    # Удаляем файл, связанный с аватаром, перед удалением объекта
        if self.avatar:
            if os.path.isfile(self.avatar.path):
                os.remove(self.avatar.path)
        super(Profile, self).delete(*args, **kwargs)
