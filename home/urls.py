from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('get-tracks/', view_tracks),
    path('my-profile/', view_my_profile),
    path('profiles/<user_id>', view_another_profile),
    path("participants/", see_users),
    path("notifications/", view_notifications),
    path("delete-readed/", delete_readed)
]