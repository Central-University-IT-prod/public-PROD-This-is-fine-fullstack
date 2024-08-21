from django.contrib import admin
from django.urls import path, include
from matching import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authenticate.urls")),
    path('teams/', include("teams.urls")),
    path('', include('home.urls')),
]
admin.site.site_header = "Админка олимпиады"
admin.site.site_title = "Matching"
if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)