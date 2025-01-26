from django import forms
from django.forms import TextInput, DateInput, Textarea
from .models import Task, Profile, Project, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomeCreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется")
        return email    
class AddProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','code','language','status','complexity']
        widgets = {
            'title': TextInput(attrs={
                'class': 'title-project',
                'placeholder': 'Введите название задачи',
                'style': 'resize: none;',
                'required': True,
            }),
            'description': Textarea(attrs={
                'class': 'desc-project',                     # Класс для CSS-стилей
                'placeholder': 'Введите описание',          # Подсказка внутри поля
                'rows': 5,                                  # Количество строк
                'cols': 50,                                 # Количество символов в строке
                'maxlength': 500,                           # Максимальная длина текста
                'required': True,                           # Поле обязательно для заполнения
                'style': 'resize: vertical;', # Inline-стили (запрет изменения размера и цвет границы)
            }),
            'code': Textarea(attrs={
                'class': 'desc-project',                     
                'placeholder': 'Введите код проекта',         
                'rows': 35,                                  
                'cols': 50,                                  
                'required': False,                           
                'style': 'resize: vertical;',
            }),

        }

class EditProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','code','language','status','complexity']
        widgets = {
            'title': TextInput(attrs={
                'class': 'title-project',
                'placeholder': 'Введите название задачи',
                'style': 'resize: none;',
                'required': True,
            }),
            'description': Textarea(attrs={
                'class': 'desc-project',                     # Класс для CSS-стилей
                'placeholder': 'Введите описание',          # Подсказка внутри поля
                'rows': 5,                                  # Количество строк
                'cols': 50,                                 # Количество символов в строке
                'maxlength': 500,                           # Максимальная длина текста
                'required': True,                           # Поле обязательно для заполнения
                'style': 'resize: vertical;', # Inline-стили (запрет изменения размера и цвет границы)
            }),
            'code': Textarea(attrs={
                'class': 'desc-project',                     
                'placeholder': 'Введите код проекта',         
                'rows': 35,                                  
                'cols': 50,                                  
                'required': False,                           
                'style': 'resize: vertical;',
            }),

        }

class EditCodeProject(forms.ModelForm):
    pass

class AddTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','status','priority']
        widgets = {
            'title': TextInput(attrs={
                'class': 'title-project',
                'placeholder': 'Введите название задачи',
                'style': 'resize: none;',
                'required': True,
            }),
            'description': Textarea(attrs={
                'class': 'desc-project',                     # Класс для CSS-стилей
                'placeholder': 'Введите описание',          # Подсказка внутри поля
                'rows': 5,                                  # Количество строк
                'cols': 50,                                 # Количество символов в строке
                'maxlength': 500,                           # Максимальная длина текста
                'required': True,                           # Поле обязательно для заполнения
                'style': 'resize: vertical;', # Inline-стили (запрет изменения размера и цвет границы)
            }),

        }

class EditTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','status','priority','assignee']
        widgets = {
            'title': TextInput(attrs={
                'class': 'title-project',
                'placeholder': 'Введите название задачи',
                'style': 'resize: none;',
                'required': True,
            }),
            'description': Textarea(attrs={
                'class': 'desc-project',                     # Класс для CSS-стилей
                'placeholder': 'Введите описание',          # Подсказка внутри поля
                'rows': 5,                                  # Количество строк
                'cols': 50,                                 # Количество символов в строке
                'maxlength': 500,                           # Максимальная длина текста
                'required': True,                           # Поле обязательно для заполнения
                'style': 'resize: vertical;', # Inline-стили (запрет изменения размера и цвет границы)
            }),

        }

class ProjectFilterForm(forms.ModelForm):
    model = Project
    fields = ['created_at']
    created_at =forms.DateField(
        widget = forms.DateInput(attrs={'type':'created_at'}),
        required=False,
        label = 'Срок выполнения'
    )

class ProfileSettings(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'style': 'display: none; text-decoration: none;' , 'class': 'id_avatar'}),
            'bio': forms.Textarea(attrs={'class': 'bio-profile', 'rows': 5, 'style': 'resize: vertical'}),
        }

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','anons','text']

class SendComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']