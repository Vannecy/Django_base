# forms.py (dans l'application "gestion")
from django import forms
from .models import Player, Trading, Team

class PlayerForm(forms.ModelForm):
    player_team = forms.ModelChoiceField(queryset=Team.objects.all(), label='Équipe')
    class Meta:
        model = Player
        fields = ['name', 'value',  'player_team']  # Ajoutez d'autres champs au besoin
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].widget = forms.NumberInput(attrs={'step': 10000})

class TradingForm(forms.ModelForm):
    class Meta:
        model = Trading
        fields = ['proposed_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proposed_value'].widget = forms.NumberInput(attrs={'step': 10000})

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']  # Ajoutez d'autres champs au besoin