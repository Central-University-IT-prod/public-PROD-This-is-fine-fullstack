from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from admin_panel.models import *
from admin_panel.models import Limitation
import json
from django.views.decorators.csrf import csrf_exempt



@login_required(redirect_field_name="next", login_url='/auth/login')
def view_teams(request):
    teams = []
    query = request.GET.get('q', "")
    max_members = Limitation.objects.all()[0].max_count_team_members
    my_team = Team.objects.filter(owner=request.user)
    another_team = TeamMember.objects.filter(user=request.user)
    if max_members is None or max_members <= 0:
        max_members = '?'
    if query:
        for team in Team.objects.filter(name__icontains=query):
            teams.append({
                "id": team.id,
                "pk": team.pk,
                "name": team.name,
                "can_add": (max_members == '?' or max_members > team.members.count() + 1) and request.user != team.owner and not my_team and not another_team,
                "max_members": max_members,
                "full_description": team.full_description,
                "who_need": ', '.join([track.name for track in team.who_need.all()]),
                "count_members": team.members.count() + 1
            })
    else:
        for team in Team.objects.all():
            teams.append({
                "id": team.id,
                "pk": team.pk,
                "name": team.name,
                "can_add": (max_members == '?' or max_members > team.members.count() + 1) and request.user != team.owner and not my_team and not another_team,
                "max_members": max_members,
                "full_description": team.full_description,
                "who_need": ', '.join([track.name for track in team.who_need.all()]),
                "count_members": team.members.count() + 1
            })
    return render(request, "view_teams.html", context={"teams": teams, "last_q": query})


@login_required(redirect_field_name="next", login_url='/auth/login')
def view_my_team(request):
    my_team = Team.objects.filter(owner=request.user)
    team_member = TeamMember.objects.filter(user=request.user)
    if my_team:
        team = my_team[0]
    elif team_member:
        team = team_member[0].team
    else:
        return render(request, "need_create_team.html")
    members = TeamMember.objects.filter(team=team)
    limit = Limitation.objects.all()[0]
    ok = True
    if limit.max_count_team_members is not None and limit.max_count_team_members != -1 and members.count() + 1 > limit.max_count_team_members:
        ok = False
    elif limit.min_count_team_members is not None and limit.min_count_team_members != -1 and members.count() + 1 < limit.min_count_team_members:
        ok = False
    elif limit.required_tracks:
        used_tracks = [member.user.profile.track.name for member in members] + [team.owner.profile.track]
        for track in [track.name for track in limit.required_tracks.all()]:
            if track not in used_tracks:
                ok = False
                break
            used_tracks.remove(track)
    elif limit.max_members_with_ununique_levels:
        levels = [member.profile.track for member in members]
        for level in level:
            if levels.count(level) > limit.max_members_with_ununique_levels:
                ok = False
            break
    context = {
        'team': team,
        'members': list(members),
        'members_users_data': [member.user for member in members],
        "owner": team.owner,
        "ok": ok,
        "who_need": ', '.join([need.name for need in team.who_need.all()])
    }
    return render(request, "team.html", context=context)


@login_required(redirect_field_name="next", login_url='/auth/login')
def create_team(request):
    tracks = [track.name for track in Track.objects.all()]
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            tracks = list(form.cleaned_data.get("tracks").split(', '))
            if tracks:
                tracks.remove("")
            team = Team.objects.create(
                name=form.cleaned_data["team_name"],
                owner=request.user,
                full_description=form.cleaned_data["team_description"],
            )
            for track in tracks:
                team.who_need.add(Track.objects.get(name=track))
            team.save()
            return redirect('/teams/my-team/')
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form, "tracks": tracks})


@login_required(redirect_field_name="next", login_url='/auth/login')
def edit_team(request):
    team = Team.objects.get(owner=request.user)
    name = team.name
    need_tracks = team.who_need.all()
    tracks = [track.name for track in Track.objects.all()]
    description = team.full_description
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            tracks = list(form.cleaned_data.get("tracks").split(', '))
            if tracks:
                tracks.remove("")
            team.name=form.cleaned_data["team_name"]
            team.full_description=form.cleaned_data["team_description"]
            team.who_need.clear()
            for track in tracks:
                team.who_need.add(Track.objects.get(name=track))
            team.save()
            return redirect('/teams/my-team/')
    else:
        form = TeamForm()
    return render(request, 'edit_team.html', {'form': form, "need_tracks": ' '.join([track.name for track in need_tracks]), "name": name, "description": description, "tracks": tracks})
@login_required(redirect_field_name="next", login_url='/auth/login')
def view_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    members = TeamMember.objects.filter(team=team)
    return render(request, 'team.html', {
        'team': team,
        'members': list(members),
        'members_usernames': [member.user for member in members],
        "owner": team.owner,
        "who_need": ', '.join([need.name for need in team.who_need.all()])
    })


@login_required(redirect_field_name="next", login_url='/auth/login')
def add_user_to_my_team(request, user_id):
    another_user = User.objects.get(pk=user_id)
    user = User.objects.get(username=request.user.username)
    team = Team.objects.get(owner=user)
    my_team = Team.objects.filter(owner=another_user)
    another_team = TeamMember.objects.filter(user=another_user)
    if not my_team and not another_team:
        TeamInvitation.objects.get_or_create(
            from_user=request.user,
            to_user=another_user,
            team=team,
            invitation_type="invite"
        )
    return HttpResponse("ok")


@login_required(redirect_field_name="next", login_url='/auth/login')
def join_to_team(request, team_id):
    team = Team.objects.get(pk=team_id)
    team_owner = team.owner
    TeamInvitation.objects.get_or_create(
        from_user=request.user,
        to_user=team_owner,
        team=team,
        invitation_type="apply"
    )
    return HttpResponse("ok")

@login_required(redirect_field_name="next", login_url='/auth/login')
def delete_team(request, team_id):
    team = Team.objects.get(pk=team_id)
    team.delete()
    return HttpResponse("ok")


@login_required(redirect_field_name="next", login_url='/auth/login')
def leave_from_team(request, team_id):
    TeamMember.objects.get(team__pk=team_id, user=request.user).delete()
    return HttpResponse("ok")


# accept / decline
@csrf_exempt
def accept_apply(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        need_user = User.objects.get(pk=json_data['user'])
        apply = TeamInvitation.objects.get(to_user=request.user, from_user__pk=json_data['user'], team__pk=json_data["team"])
        apply.status = "accepted"
        apply.save()
        TeamMember.objects.create(
            user=need_user,
            team=Team.objects.get(pk=json_data["team"])
        )
        return HttpResponse("ok")


@csrf_exempt
def decline_apply(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        apply = TeamInvitation.objects.get(to_user=request.user, from_user__pk=json_data['user'], team__pk=json_data["team"])
        apply.status = "declined"
        apply.save()
        return HttpResponse("ok")

@csrf_exempt
def accept_invite(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        apply = TeamInvitation.objects.get(to_user=request.user, from_user__pk=json_data['user'], team__pk=json_data["team"], invitation_type="invite")
        apply.status = "accepted"
        apply.save()
        TeamMember.objects.create(
            user=request.user,
            team=Team.objects.get(pk=json_data["team"])
        )
        return HttpResponse("ok")


@csrf_exempt
def decline_invite(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        apply = TeamInvitation.objects.get(to_user=request.user, from_user__pk=json_data['user'], team__pk=json_data["team"], invitation_type="invite")
        apply.status = "declined"
        apply.save()
