from django.apps import AppConfig


class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'

    def ready(self):
        try:
            from .models import Limitation
            if not Limitation.objects.exists():
                Limitation.objects.create()
        except:
            pass