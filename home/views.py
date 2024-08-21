from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from authenticate.models import Notification, Profile
from admin_panel.models import Limitation, Track
from teams.models import TeamInvitation
from django.contrib.auth.models import User
from admin_panel.models import Stack

from django.db.models import Q


@login_required(redirect_field_name="next", login_url='/auth/login')
def home(request):
    main_message = Limitation.objects.all()[0].main_message
    return render(request, "index.html", context={"main_message": main_message})

def view_tracks(request):
    tracks = [track.name for track in Track.objects.all()]
    return JsonResponse(tracks, safe=False, json_dumps_params={'ensure_ascii': False})


@login_required(redirect_field_name="next", login_url='/auth/login')
def view_my_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "profile.html", context={
            "username": profile.user.username,
            "fio": profile.fio if profile.fio else "Не указано",
            "bio": profile.bio if profile.bio else "Не указано",
            "interests": ', '.join(profile.interests) if profile.interests else "Не указано",
            "telegram_handle": profile.telegram_handle,
            "participation_class": profile.participation_class,
            "track": profile.track.name,
            "stack": ', '.join(profile.stack) if profile.stack else "Не указано",
            "phone_number": profile.phone_number if profile.phone_number else "Не указано",
            "city": profile.city if profile.city else "Не указано",
            "avatar": request.build_absolute_uri(f'/media/{profile.avatar}')
        })


@login_required(redirect_field_name="next", login_url='/auth/login')
def view_another_profile(request, user_id):
    profile = get_object_or_404(Profile, pk=user_id)
    return render(request, "profile.html", context={
        "username": profile.user.username,
        "fio": profile.fio if profile.fio else "Не указано",
        "bio": profile.bio if profile.bio else "Не указано",
        "interests": ', '.join(profile.interests) if profile.interests else "Не указано",
        "telegram_handle": profile.telegram_handle,
        "participation_class": profile.participation_class,
        "track": profile.track.name,
        "stack": ', '.join(profile.stack) if profile.stack else "Не указано",
        "phone_number": profile.phone_number if profile.phone_number else "Не указано",
        "city": profile.city if profile.city else "Не указано",
        "avatar": request.build_absolute_uri(f'/media/{profile.avatar}')
    })


@login_required(redirect_field_name="next", login_url='/auth/login')
def see_users(request):
    users = User.objects.filter(Q(team__isnull=True) & Q(my_team__isnull=True) & ~ Q(username=request.user.username))
    selected_track = ''
    stacks = [stack.name for stack in Stack.objects.all()]

    selected_stack = ''
    selected_class = ''
    selected_city = ''
    if request.method == "POST":
        users_by_track = users
        users_by_stack = users
        users_by_class = users
        users_by_city = users
        if request.POST["track"]:
            selected_track = request.POST["track"]
            users_by_track = User.objects.filter(Q(profile__track__name=request.POST["track"]) & Q(team__isnull=True) & Q(my_team__isnull=True) & ~ Q(username=request.user.username))
        if request.POST["stack"]:
            stacks = request.POST["stack"].split(', ')
            stacks.remove('')
            selected_stack = stacks
            for stack in stacks:
                users_by_stack_new = User.objects.filter(profile__stack__icontains=stack)
                users_by_stack = users_by_stack.intersection(users_by_stack_new)
        if request.POST["participant-class"]:
            selected_class = request.POST["participant-class"]
            users_by_class = User.objects.filter(Q(profile__participation_class=int(request.POST["participant-class"])) & Q(team__isnull=True) & Q(my_team__isnull=True) & ~ Q(username=request.user.username))
        if request.POST["city"]:
            selected_city = request.POST["city"]
            users_by_city = User.objects.filter(Q(profile__city=request.POST["city"]) & Q(team__isnull=True) & Q(my_team__isnull=True) & ~ Q(username=request.user.username))
        
        users = users_by_track.intersection(users_by_stack.intersection(users_by_class.intersection(users_by_city)))
    tracks = [track.name for track in Track.objects.all()]
    return render(request, "participants.html", context={
        "users": users,
        "tracks": tracks,
        "selected_track": selected_track,
        "selected_stack": selected_stack,
        "selected_participant_class": selected_class,
        "selected_city": selected_city,
        "stacks": stacks})


@login_required(redirect_field_name="next", login_url='/auth/login')
def view_notifications(request):
    notifications_apply = TeamInvitation.objects.filter(to_user=request.user, invitation_type="apply", status="pending")
    notifications_from_apply_denied = TeamInvitation.objects.filter(from_user=request.user, status="declined", invitation_type="apply")
    answer_denied = []
    for i in notifications_from_apply_denied:
        answer_denied.append({
            "to_user": i.to_user,
            "from_user": i.from_user,
            "team": i.team
        }
        )
    notifications_from_apply_accepted = TeamInvitation.objects.filter(from_user=request.user, status="accepted", invitation_type="apply")
    answer_accepted = []
    for i in notifications_from_apply_accepted:
        answer_accepted.append({
            "to_user": i.to_user,
            "from_user": i.from_user,
            "team": i.team
        }
        )

    invite_need = TeamInvitation.objects.filter(to_user=request.user, invitation_type="invite", status="pending")
    invite_from_denied = TeamInvitation.objects.filter(from_user=request.user, status="declined", invitation_type="invite")
    invite_denied = []
    for i in invite_from_denied:
        invite_denied.append({
            "to_user": i.to_user,
            "from_user": i.from_user,
            "team": i.team
        }
        )
    invite_from_acepted = TeamInvitation.objects.filter(from_user=request.user, status="accepted", invitation_type="invite")
    invite_acepted = []
    for i in invite_from_acepted:
        invite_acepted.append({
            "to_user": i.to_user,
            "from_user": i.from_user,
            "team": i.team
        }
        )
    
    notifications_by_organizators = Notification.objects.filter(user=request.user, read=False)
    notifications_by_organizators_text = []
    for i in notifications_by_organizators:
        notifications_by_organizators_text.append(
            {
                "text": i.message,
                "title": i.title
            }
        )




    notifications_from_apply_denied_readed = TeamInvitation.objects.filter(from_user=request.user, status="declined_closed", invitation_type="apply")
    answer_denied_readed = []
    for i in notifications_from_apply_denied_readed:
        answer_denied_readed.append({
            "to_user": i.to_user,
            "from_user": i.from_user,
            "team": i.team
        }
        )
    notifications_from_apply_accepted_readed = TeamInvitation.objects.filter(from_user=request.user, status="accepted_closed", invitation_type="apply")
    answer_accepted_readed = []
    for i in notifications_from_apply_accepted_readed:
        answer_accepted_readed.append({
            "to_user": i.to_user,
            "from_user": i.from_user,
            "team": i.team
        }
        )

    invite_from_denied_readed = TeamInvitation.objects.filter(from_user=request.user, status="declined_closed", invitation_type="invite")
    invite_denied_readed = []
    for i in invite_from_denied_readed:
        invite_denied_readed.append({
            "to_user": i.to_user,
            "from_user": i.from_user,
            "team": i.team
        }
        )
    invite_from_acepted_readed = TeamInvitation.objects.filter(from_user=request.user, status="accepted_closed", invitation_type="invite")
    invite_acepted_readed = []
    for i in invite_from_acepted_readed:
        invite_acepted_readed.append({
            "to_user": i.to_user,
            "from_user": i.from_user,
            "team": i.team
        }
        )
    
    notifications_by_organizators_readed = Notification.objects.filter(user=request.user, read=True)
    notifications_by_organizators_text_readed = []
    for i in notifications_by_organizators_readed:
        notifications_by_organizators_text_readed.append(
            {
                "text": i.message,
                "title": i.title
            }
        )

    notifications_by_organizators.update(read=True)
    notifications_from_apply_denied.update(status="declined_closed")
    invite_from_acepted.update(status="accepted_closed")
    notifications_from_apply_accepted.update(status='accepted_closed')
    invite_from_denied.update(status="declined_closed")


    return render(request, "alerts.html", context={
        "notifications_apply": notifications_apply,
        "your_denied": answer_denied,
        "your_acepted": answer_accepted,
        "invite_need_apply": invite_need,
        "invite_denied": invite_denied,
        "invite_acepted": invite_acepted,
        "notifications_by_organizator": notifications_by_organizators_text,
        "your_denied_readed": answer_denied_readed,
        "your_acepted_readed": answer_accepted_readed,
        "invite_denied_readed": invite_denied_readed,
        "invite_acepted_readed": invite_acepted_readed,
        "notifications_by_organizator_readed": notifications_by_organizators_text_readed,
        "was_readed": answer_denied_readed or answer_accepted_readed or invite_denied_readed or invite_acepted_readed or notifications_by_organizators_text_readed
    })


@login_required(redirect_field_name="next", login_url='/auth/login')
def delete_readed(request):
    notifications_from_apply_denied_readed = TeamInvitation.objects.filter(from_user=request.user, status="declined_closed", invitation_type="apply")
    notifications_from_apply_accepted_readed = TeamInvitation.objects.filter(from_user=request.user, status="accepted_closed", invitation_type="apply")
    invite_from_denied_readed = TeamInvitation.objects.filter(from_user=request.user, status="declined_closed", invitation_type="invite")
    invite_from_acepted_readed = TeamInvitation.objects.filter(from_user=request.user, status="accepted_closed", invitation_type="invite")
    
    notifications_by_organizators_readed = Notification.objects.filter(user=request.user, read=True)
    notifications_by_organizators_readed.delete()
    notifications_from_apply_denied_readed.delete()
    notifications_from_apply_accepted_readed.delete()
    invite_from_denied_readed.delete()
    invite_from_acepted_readed.delete()

    return redirect("/notifications/")