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
        ('C', 'Си'),
        ('C++', 'Си плюс плюс'),
        ('C#', 'Си шарп'),
        ('Go', 'Го'),
        ('Java', 'Джава'),
        ('JavaScript', 'Джаваскрипт'),
        ('Kotlin', 'Котлин'),
        ('PHP', 'ПХП'),
        ('Python', 'Пайтон'),
        ('Ruby', 'Руби'),
        ('Rust', 'Раст'),
        ('Scala', 'Скала'),
        ('TypeScript', 'Тайпскрипт'),
        ('Swift', 'Свифт'),
        ('R', 'Эр'),
        ('Dart', 'Дарт'),
        ('Shell', 'Шелл'),
        ('Haskell', 'Хаскелл'),
        ('Perl', 'Перл'),
        ('Lua', 'Луа'),
        ('Elixir', 'Эликсир'),
        ('Erlang', 'Эрланг'),
        ('Visual Basic', 'Вижуал Бейсик'),
        ('Objective-C', 'Обжектив-Си'),
        ('Fortran', 'Фортран'),
        ('COBOL', 'Кобол'),
        ('F#', 'Эф шарп'),
        ('SQL', 'Эс-Кью-Эл'),
        ('Julia', 'Джулия'),
        ('Racket', 'Ракет'),
        ('Tcl', 'Тикл'),
        ('VHDL', 'Ви-Эйч-Ди-Эл'),
        ('Verilog', 'Верилог'),
        ('Assembly', 'Ассемблер'),
        ('Prolog', 'Пролог'),
        ('Ada', 'Ада'),
        ('Matlab', 'Матлаб'),
        ('Crystal', 'Кристал'),
        ('D', 'Ди'),
        ('Groovy', 'Груви'),
        ('Nim', 'Ним'),
        ('Solidity', 'Солидити'),
        ('COQ', 'Кок'),
        ('APL', 'Эй-Пи-Эль'),
        ('Ballerina', 'Баллерина'),
        ('Not specified', 'Не указан'),
    ]

class Status(models.Model):
    STATUS_CHOICES = [('Complited','Выполнено'),
                      ('In Development','В разработке'),
                      ('Waiting','Ожидает')
                      ]
    
    PRIORITY_CHOICES = [('Low','Низкий'),
                        ('Average','Cредний'),
                        ('High','Высокий'),
                        ('Not specified','Не указан')
                        ]
    
    BLACKLIST_CHOICES = [('Заблокирован','Baned'),
                         ('Не заблокирован','Not baned'),
                         ]
    
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # tasks = models.ManyToManyField(Task, related_name='p_tasks')
    code = models.TextField()
    language = models.CharField(max_length=50, choices=Language.LANGUAGE_CHOICES, default='Not specified')
    status = models.CharField(max_length=50,choices=Status.STATUS_CHOICES, default='Waiting')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='p_owner')
    participants = models.ManyToManyField(User, blank=True, related_name='p_participants')
    created_at = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    # updated_at = models.DateField() #Реализовать дату последнего обновления

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='t_creator')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='t_project')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name='t_assignee')
    priority = models.CharField(max_length=50, choices=Status.PRIORITY_CHOICES, default='Not specified')
    status = models.CharField(max_length=50,choices=Status.STATUS_CHOICES, default='Waiting')
    created_at = models.DateField(auto_now_add=True)
    # updated_at = models.DateField() #Реализовать дату последнего обновления

    def __str__(self):
        return self.title

class Profile(models.Model):
    puser = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='./profile_avatars/', blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, choices=Role.ROLE_CHOICES, default='Executor')
    status = models.CharField(max_length=50, choices=Status.BLACKLIST_CHOICES, default='Not baned')

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
