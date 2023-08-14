# forms.py (dans l'application "gestion")
from django import forms
from .models import Player, Trading, Team
from django.contrib.auth.models import User 
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

class ComposeMessageForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), label='Receiver')
    subject = forms.CharField(max_length=100, label='Subject')
    text = forms.CharField(widget=forms.Textarea, label='Message')
    trading_number = forms.IntegerField(label='Trading Number')
    proposed_amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Proposed Amount')