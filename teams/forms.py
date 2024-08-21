from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TeamForm(forms.Form):
    team_name = forms.CharField(max_length=100, label="Название", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}))
    team_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Python, Django, React'}), required=False)
    tracks = forms.CharField(label="Полное описание", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Полное описание'}))
    

class SearchForm(forms.Form):
    query = forms.CharField(label='Название команды', max_length=100)
