from django import forms
from django.forms import TextInput, DateInput, Textarea
from .models import Task, Profile, Project
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomeCreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AddProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','code','language','status','start_date','end_date']
        widgets = {
            'title': TextInput(attrs={
                'class': 'title-project',
                'placeholder': 'Введите название задачи',
                'style': 'resize: none; border-color: green;',
                'required': True,
            }),
            'description': Textarea(attrs={
                'class': 'desc-project',                     # Класс для CSS-стилей
                'placeholder': 'Введите описание',          # Подсказка внутри поля
                'rows': 5,                                  # Количество строк
                'cols': 50,                                 # Количество символов в строке
                'maxlength': 500,                           # Максимальная длина текста
                'required': True,                           # Поле обязательно для заполнения
                'style': 'resize: vertical; border-color: green;'# Inline-стили (запрет изменения размера и цвет границы)
            }),
            'code': Textarea(attrs={
                'class': 'desc-project',                     # Класс для CSS-стилей
                'placeholder': 'Введите код проекта',          # Подсказка внутри поля
                'rows': 35,                                  # Количество строк
                'cols': 50,                                 # Количество символов в строке                           # Максимальная длина текста
                'required': False,                           # Поле обязательно для заполнения
                'style': 'resize: vertical; border-color: green;'# Inline-стили (запрет изменения размера и цвет границы)
            }),
            'start_date': DateInput(attrs={
                'class': 'desc-project', 
                'type':'date',
                'required': False,
            }),
            'end_date': DateInput(attrs={
                'class': 'desc-project', 
                'type':'date',
                'required': False,
            })

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
    model = Profile
    fields = ['user', 'bio', 'avatar']
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
# class SettingsProfile(forms.ModelForm):
 