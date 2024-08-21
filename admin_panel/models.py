from django.db import models
from tinymce.models import HTMLField


class Track(models.Model):
    name = models.CharField("Название", max_length=255)
    
    def __str__(self) -> str:
        return self.name


class Stack(models.Model):
    name = models.CharField("Название", max_length=255)
    
    def __str__(self) -> str:
        return self.name


class Limitation(models.Model):
    max_count_team_members = models.IntegerField("Максимальное кол-во участинков", blank=True, null=True)
    min_count_team_members = models.IntegerField("Минимальное кол-во участинков", blank=True, null=True)
    required_tracks = models.ManyToManyField(Track, blank=True, null=True, verbose_name="Обязательные треки в команде")
    max_members_with_ununique_levels = models.IntegerField("Максимальное кол-во участников с одинаковыми классами участия", blank=True, null=Track)
    main_message = HTMLField("Сообщение на главном экране", default="<h1>Hello world</h1>")
    _singleton = models.BooleanField(default=True, editable=False, unique=True)

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self) -> str:
        return 'Настройки'