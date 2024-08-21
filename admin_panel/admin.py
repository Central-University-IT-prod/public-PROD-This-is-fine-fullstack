from django.contrib import admin
from .models import *
from django.shortcuts import HttpResponse
import csv
from django.db.models import Q


from authenticate.models import Profile
from teams.models import Team, TeamMember

admin.site.register(Track)
admin.site.register(Stack)
# admin.site.register(Limitation)

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path


@admin.register(Limitation)
class LoginMonitorAdmin(admin.ModelAdmin):
    change_list_template = "admin/monitor_change_list.html"

    def get_urls(self):
        urls = super(LoginMonitorAdmin, self).get_urls()
        custom_urls = [
            path('test/', self.process_import, name='process_import'),
            path('auto/', self.auto_distribute, name='auto_distribute')]
        return custom_urls + urls

    def process_import(self, request):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="profiles_data.csv"'},
        )

        writer = csv.writer(response)
        
        writer.writerow(['fio', 'username', 'team', 'telegram', 'participation_class', 'phone_number', 'city'])

        for obj in Profile.objects.all():
            my_team = Team.objects.filter(owner=obj.user)
            another_team = TeamMember.objects.filter(user=obj.user)
            if my_team:
                team = my_team[0].name
            elif another_team:
                team = another_team[0].team.name
            else:
                team = ''
            writer.writerow([ obj.fio, obj.user.username, team, obj.telegram_handle,
                            obj.participation_class, obj.phone_number, obj.city])
        
        return response


        # self.message_user(request, f"создано 123 новых записей")
        # return HttpResponseRedirect("../")

    def auto_distribute(self, request):
        limitation = Limitation.objects.first()
        max_count = limitation.max_count_team_members
        participants = Profile.objects.filter(user__team=None)
        if max_count < 1:
            c = 0
            for p in participants:
                if Team.objects.filter(owner=p.user):
                    continue
                if c == 0:
                    team = Team.objects.create(
                        owner=p.user,
                        name=f"{p.user.username}'s team"
                    )
                else:
                    TeamMember.objects.create(
                        user=p.user,
                        team=team
                    )
                c += 1
        else:
            c = 0
            for p in participants:
                if Team.objects.filter(owner=p.user):
                    continue
                if c == 0:
                    print("CREATE_TEAM")
                    team = Team.objects.create(
                        owner=p.user,
                        name=f"{p.user.username}'s team"
                    )
                else:
                    print("ADD_TO_TEAM")
                    TeamMember.objects.create(
                        user=p.user,
                        team=team
                    )
                c += 1
                if c > max_count:
                    c = 0
        
        
        self.message_user(request, f"Распредедение завершено!")
        return HttpResponseRedirect("../")