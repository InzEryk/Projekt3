from django import forms
from django.forms import ModelForm
from .models import Tournament, Winner, Player, History


class TournamentForm(ModelForm):

    class Meta:
        model = Tournament
        fields = ('name', 'started_date', 'number_of_players')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'started_date': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Started date as 2022-06-13 21:00'}),
            'number_of_players': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number from range 4 - 64'}),
        }


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ('tournament', 'name',)


class HistoryForm(ModelForm):
    class Meta:
        model = History
        fields = ('date',)


class WinnerForm(ModelForm):
    class Meta:
        model = Winner
        fields = ('player_one_score', 'player_two_score',)

    def clean(self):
        form_data = self.cleaned_data
        if form_data["player_one_score"] == form_data["player_two_score"]:
            self._errors["player_one_score"] = ["Draw is not an option"]
            del form_data["player_one_score"]
        return form_data
