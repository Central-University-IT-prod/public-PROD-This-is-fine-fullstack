from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import AvaliableEmail
from admin_panel.models import Track, Stack
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files.base import ContentFile
import openai
import requests

from .forms import *


def login_view(request):
    login_data = ''
    errors = []
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login_data = form.cleaned_data['login']
            user = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.GET.get("next"):
                        return redirect(request.GET.get("next"))
                    else:
                        return redirect('/')
                else:
                    errors.append("Ваш аккаунт заблокирован!")

            else:
                errors.append("Неверный логин/пароль!")

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "login": login_data, "errors": errors})


def register_view(request):
    tracks = [track.name for track in Track.objects.all()]
    stacks = [stack.name for stack in Stack.objects.all()]
    errors = []
    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            username = form.cleaned_data.get('login')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password != password2:
                errors.append('Пароли не совпадают!')
                pass
            else:
                if User.objects.filter(username=username) or User.objects.filter(email=email):
                    errors.append('Аккаунт с таким именем пользователя уже существует!')
                    pass
                # elif not AvaliableEmail.objects.filter(email=email):
                #     # Нет почты
                #     errors.append("Вашего email нет в списках участников!")
                #     pass
                else:
                    # AvaliableEmail.objects.get(email=email).delete()
                    user = User.objects.create_user(username=username, email=email, password=password)
                    fio = form.cleaned_data.get('fio')
                    bio = form.cleaned_data.get('bio')
                    participation_class = form.cleaned_data.get('participation_class')
                    track = Track.objects.get(name=form.cleaned_data.get('track'))
                    phonenumber = form.cleaned_data.get('phonenumber')
                    city = form.cleaned_data.get('city')
                    telegram = form.cleaned_data.get("telegram")
                    interests = list(form.cleaned_data.get("interests").split(', '))
                    stack = list(form.cleaned_data.get("stack").split(', '))
                    if interests:
                        interests.remove('')
                    else:
                        interests = []
                    if stack:
                        stack.remove('')
                    else:
                        stack = []
                    profile = Profile.objects.create(
                        user=user,
                        fio=fio,
                        bio=bio,
                        participation_class=participation_class,
                        track=track,
                        phone_number=phonenumber,
                        city=city,
                        telegram_handle=telegram,
                        stack=stack,
                        interests=interests
                    )
                    if form.cleaned_data.get("avatar"):
                        profile.avatar = form.cleaned_data.get("avatar")
                        profile.save()
                    else:
                        response = requests.get(form.cleaned_data["avatarai"])
                        content = ContentFile(response.content)
                        profile.avatar.save(f'{username}.png', content=content, save=True)
                        profile.save()
                    login(request, user)
                    return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, "tracks": tracks, "stacks": stacks, "errors": errors})


@login_required(redirect_field_name="next", login_url='/auth/login')
def edit_profile(request):
    tracks = [track.name for track in Track.objects.all()]
    errors = []
    stacks = [stack.name for stack in Stack.objects.all()]
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('login')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password != password2:
                errors.append('Пароли не совпадают!')
                pass
            else:
                if User.objects.filter(Q(username=username)& ~Q(pk=request.user.pk)) or User.objects.filter(Q(email=email)& ~Q(pk=request.user.pk)):
                    errors.append('Аккаунт с таким именем пользователя уже существует!')
                    pass
                else:
                    # user = User.objects.create_user(username=username, email=email, password=password)
                    user = User.objects.get(pk=request.user.pk)
                    user.email = email
                    user.username = username
                    user.set_password(password)
                    user.save()
                    fio = form.cleaned_data.get('fio')
                    bio = form.cleaned_data.get('bio')
                    participation_class = form.cleaned_data.get('participation_class')
                    track = Track.objects.get(name=form.cleaned_data.get('track'))
                    phonenumber = form.cleaned_data.get('phonenumber')
                    city = form.cleaned_data.get('city')
                    telegram = form.cleaned_data.get("telegram")
                    interests = list(form.cleaned_data.get("interests").split(', '))
                    stack = list(form.cleaned_data.get("stack").split(', '))
                    if interests:
                        interests.remove('')
                    else:
                        interests = []
                    if stack:
                        stack.remove('')
                    else:
                        stack = []
                    profile_filter = Profile.objects.filter(pk=profile.pk)
                    profile.fio=fio
                    profile.bio=bio
                    profile.participation_class=participation_class
                    profile.track=track
                    profile.phone_number=phonenumber
                    profile.city=city
                    profile.telegram_handle=telegram
                    profile.stack=stack
                    profile.interests=interests
                    if form.cleaned_data.get("avatar"):
                        profile.avatar = form.cleaned_data.get("avatar")
                    login(request, user)
                    profile.save()
                    return redirect('/my-profile/')
    else:
        form = RegisterForm()
    return render(request, 'edit_user.html', {
        'form': form,
        "tracks": tracks,
        "errors": errors,
        "fio": profile.fio,
        "bio": profile.bio,
        "email": request.user.email,
        "participation_class": profile.participation_class,
        "old_track": profile.track.name,
        "phone_number": profile.phone_number if profile.phone_number is not None else "",
        "city": profile.city if profile.city is not None else "",
        "telegram_handle": profile.telegram_handle,
        "stack": profile.stack,
        "interests": profile.interests,
        "username": request.user.username,
        "stacks": stacks
    })


def logout_view(request):
    logout(request)
    return redirect("/")


def generate_avatar(request, username):
    client = openai.Client(api_key='XXX', base_url='https://api.shard-ai.xyz/v1', max_retries=50)
    url = client.images.generate(prompt=f"avatar for username {username}", model="sdxl",  size="256x256",n=1).data[0].url
    return HttpResponse(url)

def license(request):
    return render(request, "license.html")