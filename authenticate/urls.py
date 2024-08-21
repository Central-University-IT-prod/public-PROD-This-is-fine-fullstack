from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view),
    path('register/', register_view),
    path("edit-profile/", edit_profile),
    path("generate_avatar/<username>", generate_avatar),
    path('logout/', logout_view),
    path("license/", license)
]