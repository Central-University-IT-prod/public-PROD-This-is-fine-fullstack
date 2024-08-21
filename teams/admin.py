from django.contrib import admin
from .models import *

# admin.site.register(Team)
# admin.site.register(TeamMember)
admin.site.register(TeamInvitation)

class TeamMemberInline(admin.TabularInline):
    model = TeamMember


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [
        TeamMemberInline,
    ]
