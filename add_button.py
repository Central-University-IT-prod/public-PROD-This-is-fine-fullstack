
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path


@admin.register(Track)
class LoginMonitorAdmin(admin.ModelAdmin):
    change_list_template = "admin/monitor_change_list.html"

    def get_urls(self):
        urls = super(LoginMonitorAdmin, self).get_urls()
        custom_urls = [
            path('test/', self.process_import, name='process_import')]
        return custom_urls + urls

    def process_import(self, request):
        self.message_user(request, f"создано 123 новых записей")
        return HttpResponseRedirect("../")