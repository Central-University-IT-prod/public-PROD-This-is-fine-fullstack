from django.db import models
from django.contrib.auth.models import User
from admin_panel.models import Track


class Profile(models.Model):
    fio = models.CharField("ФИО", max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField("О себе", blank=True, null=True)
    interests = models.JSONField("Интересы", default=[], blank=True, null=True)
    telegram_handle = models.CharField("Ник телеграм", max_length=255)
    participation_class = models.IntegerField("Класс учатия", default=9)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, verbose_name="Трек")
    stack = models.JSONField("Стек", default=[], blank=True, null=True)
    phone_number = models.CharField("Номер телефона", max_length=20, blank=True, null=True)
    city = models.CharField("Город", max_length=255, blank=True, null=True)
    avatar = models.ImageField("Аватар", upload_to='avatars/', default="avatar.png")

    def __str__(self):
        return f"{self.user.username}"


class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Уведомление для {self.user.username}: {self.title}"


class AvaliableEmail(models.Model):
    email = models.EmailField("Адрес электронной почты")

    def __str__(self) -> str:
        return self.email