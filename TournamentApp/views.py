from django.shortcuts import render, redirect, get_object_or_404
import datetime
from .functions import players_in_round, number_of_rounds, number_of_duels
from .models import Tournament, MatchPair, Player
from .forms import TournamentForm, PlayerForm, WinnerForm, HistoryForm
from django.contrib import messages


def show_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    players = tournament.player_set.all()
    return render(request, 'tournament/show_tournament.html', {'tournament': tournament, 'players': players})


def all_tournaments(request):
    tournament_list = Tournament.objects.all()
    return render(request, 'tournament/tournament_list.html', {'tournament_list': tournament_list})


def tournament_restricted(request):
    tournament_list_restricted = Tournament.objects.all()
    return render(request, 'tournament/tournament_list_restricted.html', {'tournament_list_restricted': tournament_list_restricted})


def home(request):
    return render(request, 'tournament/home.html', {})


def add_tournament(request):
    submitted = False
    if request.method == "POST":
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.owner = request.user.id
            tournament.save()
            messages.success(request, 'New tournament created')
            return redirect('tournament_list')
    else:
        form = TournamentForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'tournament/add_tournament.html', {'form': form, 'submitted': submitted})


def edit_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    form = TournamentForm(request.POST or None, instance=tournament)
    given_number = int(form['number_of_players'].value())
    size = tournament.number_of_players
    print(given_number)
    if request.user.id == tournament.owner or request.user.is_superuser:
        if form.is_valid():
            if given_number < size:
                messages.success(request, ("Nie można dać mniejszej ilości graczy"))
                return redirect('tournament_list')
            else:
                form.save()
                messages.success(request, ("Tournament updated"))
                return redirect('tournament_list')
    else:
        messages.success(request, ("You are not an owner or superuser"))
        return redirect('tournament_list')
    return render(request, 'tournament/edit_tournament.html',
                  {'tournament': tournament,
                   'form': form})


def delete_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    if request.user.id == tournament.owner or request.user.is_superuser:
        tournament.delete()
        messages.success(request, ("Tournament deleted"))
        return redirect('tournament_list')
    else:
        messages.success(request, ("You are not an owner or superuser"))
        return redirect('tournament_list')


def add_player(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        tournament = Tournament.objects.get(pk=form['tournament'].value())
        players_count = tournament.player_set.all().count()
        size = tournament.number_of_players
        if request.user.id == tournament.owner or request.user.is_superuser:
            if players_count == size:
                messages.success(request, ("Osiagnieto limit graczy"))
                return redirect('tournament_list')
            else:
                if form.is_valid():
                    form.save()
                    messages.success(request, 'New player created')
                    return redirect('tournament_list')
        else:
            messages.success(request, ("You are not an owner or superuser"))
            return redirect('tournament_list')
    else:
        form = PlayerForm
    return render(request, 'tournament/add_tournament.html', {'form': form})


def update_player(request, player_id):
    player = Player.objects.get(pk=player_id)
    form = PlayerForm(request.POST or None, instance=player)
    tournament = Tournament.objects.get(pk=form['tournament'].value())
    players_count = tournament.player_set.all().count()
    size = tournament.number_of_players
    if request.user.id == tournament.owner or request.user.is_superuser:
        if form.is_valid():
            if players_count >= size:
                messages.success(request, ("Osiagnieto limit graczy"))
                return redirect('tournament_list')
            else:
                form.save()
                messages.success(request, ("Player updated"))
                return redirect('tournament_list')
    else:
        messages.success(request, ("You are not a superuser"))
        return redirect('tournament_list')
    return render(request, 'tournament/update_player.html',
                  {'player': player,
                   'form': form})


def delete_player(request, player_id):
    player = Player.objects.get(pk=player_id)
    owner = player.tournament.owner
    if request.user.id == owner or request.user.is_superuser:
        player.delete()
        messages.success(request, ("Player deleted"))
        return redirect('tournament_list')
    else:
        messages.success(request, ("You are not a superuser"))
        return redirect('tournament_list')


def bracket_tournament(request, tournament_id):
    tournament = Tournament.objects.filter(id=tournament_id)
    duels = MatchPair.objects.filter(tournament=tournament_id)
    winners = []
    bracket_size = []
    bracket = []
    number_of_duels(winners, duels)
    size = tournament[0].number_of_players
    round_number = int(size / 2)
    number_of_rounds(round_number, bracket_size)
    duel_number = []
    duel = list(duels)
    while bracket_size:
        for i in range(bracket_size[0]):
            duel_number.append(duel.pop(0))
        bracket.append(duel_number)
        duel_number = []
        bracket_size.pop(0)
    return render(request, 'tournament/bracket.html', {'size': size, 'bracket': bracket, 'tournament': tournament, 'winner': winners})


def edit_bracket_tournament(request, tournament_id):
    tournament_owner = Tournament.objects.get(pk=tournament_id)
    tournament = Tournament.objects.filter(id=tournament_id)
    duels = MatchPair.objects.filter(tournament=tournament_id)
    if request.user.id == tournament_owner.owner or request.user.is_superuser:
        winners = []
        bracket_size = []
        bracket = []
        number_of_duels(winners, duels)
        size = tournament[0].number_of_players
        round_number = int(size / 2)
        number_of_rounds(round_number, bracket_size)
        duel_number = []
        duel = list(duels)
        while bracket_size:
            for i in range(bracket_size[0]):
                duel_number.append(duel.pop(0))
            bracket.append(duel_number)
            duel_number = []
            bracket_size.pop(0)
        return render(request, 'tournament/edit_bracket.html', {'size': size, 'bracket': bracket, 'tournament': tournament, 'winner': winners})
    else:
        messages.success(request, ("You are not an owner or superuser"))
        return redirect('tournament_list')


def duel_winner(request, id):
    duel = MatchPair.objects.filter(id=id)
    if duel[0].player_one == None or duel[0].player_two == None:
        return redirect('/editbracket' + str(duel[0].tournament.id) + '/')
    if request.method == 'POST':
        form = WinnerForm(request.POST)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.duel = duel[0]
            saving.save()
            players_in_round(id)
            return redirect('/bracket/' + str(duel[0].tournament.id) + '/')
        else:
            messages.success(request, ("Error score"))
            print(form.errors)
    else:
        form = WinnerForm()
    return render(request, 'tournament/winner.html', {'form': form})


def history(request):
    tournament = Tournament.objects.all()
    form = HistoryForm(request.POST)
    date = datetime.datetime.now()
    if form.is_valid():
        date_string = form['date'].value()
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M")
        print(date_string)
        print(date)
        form.save()
        messages.success(request, 'Sorted')
        return redirect('history')
    return render(request, 'tournament/history.html', {'history': tournament, 'form': form, 'date': date})


def open_close(request):
    tournament = get_object_or_404(Tournament, pk=request.GET.get('tournament_id'))
    if request.user.id == tournament.owner or request.user.is_superuser:
        tournament.closed = True
        tournament.save()
        return redirect('tournament_list')
    else:
        messages.success(request, ("You are not an owner or superuser"))
        return redirect('tournament_list')


def show_history(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    players = tournament.player_set.all()
    return render(request, 'tournament/show_history.html', {'tournament': tournament, 'players': players})
