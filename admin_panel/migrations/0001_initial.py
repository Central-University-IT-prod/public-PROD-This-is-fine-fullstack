# Generated by Django 5.0.3 on 2024-03-31 10:57

import admin_panel.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Limitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_count_team_members', models.IntegerField(blank=True, null=True, verbose_name='Максимальное кол-во участинков')),
                ('min_count_team_members', models.IntegerField(blank=True, null=True, verbose_name='Минимальное кол-во участинков')),
                ('max_members_with_ununique_levels', models.IntegerField(blank=True, null=admin_panel.models.Track, verbose_name='Максимальное кол-во участников с одинаковыми классами участия')),
                ('_singleton', models.BooleanField(default=True, editable=False, unique=True)),
                ('required_tracks', models.ManyToManyField(blank=True, null=True, to='admin_panel.track', verbose_name='Обязательные треки в команде')),
            ],
            options={
                'verbose_name': 'Настройки',
                'verbose_name_plural': 'Настройки',
            },
        ),
    ]
