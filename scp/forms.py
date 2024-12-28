from django import forms
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
        fields = ['title','description','code','language','status','owner','participants','start_date','end_date']

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
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
# class SettingsProfile(forms.ModelForm):
 