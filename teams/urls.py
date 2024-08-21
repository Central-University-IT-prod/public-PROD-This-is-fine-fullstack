from django.urls import path
from .views import *


urlpatterns = [
    path("", view_teams),
    path("my-team/", view_my_team),
    path('create_team/', create_team),
    path('<int:team_id>/', view_team, name='view_team'),
    path("create-team/", create_team),
    path("edit-team/", edit_team),
    path("add-to-team/<user_id>", add_user_to_my_team),
    path("join-to-team/<team_id>", join_to_team),
    path("delete-team/<team_id>", delete_team),
    path("leave-from-team/<team_id>", leave_from_team),
    path("accept-apply/", accept_apply),
    path("decline-apply/", decline_apply),
    path("accept-invite/", accept_invite),
    path("decline-invite/", decline_invite),
]