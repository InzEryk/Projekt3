from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import MyUser


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('user_name', 'email', 'birthday')


class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ('user_name', 'email', 'birthday')