from django import forms
from .models import Profile


class LoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    login = forms.CharField(label="Login", max_length=100)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password2", widget=forms.PasswordInput())
    fio = forms.CharField(label="FIO", widget=forms.TextInput())
    bio = forms.CharField(label="BIO", widget=forms.TextInput(), required=False)
    participation_class = forms.IntegerField(label="Класс учатия")
    track = forms.CharField(label="Track")
    telegram = forms.CharField(label="Telegram")
    phonenumber = forms.CharField(label="Phone", required=False)
    avatar = forms.ImageField(label="Avatar", required=False)
    city = forms.CharField(label="City", required=False)
    interests = forms.CharField(required=False)
    stack = forms.CharField(required=False)
    avatarai = forms.CharField(required=False)
