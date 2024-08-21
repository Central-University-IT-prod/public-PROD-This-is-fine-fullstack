from django.db import models
from django.contrib.auth.models import User
from authenticate.models import Profile
from admin_panel.models import Track


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    who_need = models.ManyToManyField(Track, verbose_name="Кто нужен")
    full_description = models.TextField(verbose_name="Полное описание", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="my_team")

    class Meta:
        unique_together = ['name']

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="team")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Команда", related_name="members")
    date_joined = models.DateField(auto_now_add=True, verbose_name="Дата присоединения")

    class Meta:
        unique_together = ['user', 'team']

    def __str__(self):
        return f"{self.user.username} в команде {self.team.name}"
    

class TeamInvitation(models.Model):
    INVITE = 'invite'
    APPLY = 'apply'
    INVITATION_CHOICES = [
        (INVITE, 'Приглашение'),
        (APPLY, 'Заявка')
    ]

    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    STATUS_CHOICES = [
        (PENDING, 'Ожидает'),
        (ACCEPTED, 'Принято'),
        (DECLINED, 'Отклонено'),
        ("closed", "Закрыто")
    ]

    from_user = models.ForeignKey(User, related_name="invitations_sent", on_delete=models.CASCADE, verbose_name="Отправитель")
    to_user = models.ForeignKey(User, related_name="invitations_received", on_delete=models.CASCADE, verbose_name="Получатель")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="invitations", verbose_name="Команда")
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    invitation_type = models.CharField(max_length=6, choices=INVITATION_CHOICES, default=INVITE, verbose_name="Тип")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=PENDING, verbose_name="Статус")

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.team.name})"

    class Meta:
        unique_together = ['from_user', 'to_user', 'team', 'invitation_type']
