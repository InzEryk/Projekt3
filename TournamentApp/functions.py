import math
import random
from .models import Player, MatchPair, Winner


def random_player(number):
    index = random.randrange(0, len(number))
    return number.pop(index)


def create_bracket(tournament_id):
    player = Player.objects.filter(tournament=tournament_id[0])
    variable = 1
    players = []
    list_size = []
    number_of_players = len(player)
    round_number = int(number_of_players / 2)
    number_of_rounds(round_number, list_size)
    list_size.pop(0)
    for person in player:
        players.append(person)
    while player:
        if len(players) > 0:
            player_one = random_player(players)
            player_two = random_player(players)
            duel = MatchPair(player_one=player_one, player_two=player_two,
                             tournament=tournament_id[0], stage=int(number_of_players / 2),
                             duelNumber=variable, open=True)
            duel.save()
            variable += 1
        elif variable < len(player):
            for amount in list_size:
                for digit in range(1, amount + 1):
                    duel = MatchPair(player_one=None, player_two=None,
                                     tournament=tournament_id[0], stage=amount,
                                     duelNumber=digit, open=False)
                    duel.save()
                    variable += 1
        else:
            break


def players_in_round(id):
    duel = MatchPair.objects.filter(id=id)
    result = Winner.objects.filter(duel=duel[0].id)
    if result[0].player_one_score > result[0].player_two_score:
        if duel[0].duelNumber % 2 == 1 or duel[0].duelNumber == 1:
            number = int(math.ceil(duel[0].duelNumber / 2))
            update_duel = player_in_bracket(number, duel)
            update_duel.update(player_one=duel[0].player_one)
            duel.update(open=False)
            edit_duel(update_duel)
        else:
            number = int(duel[0].duelNumber / 2)
            update_duel = player_in_bracket(number, duel)
            update_duel.update(player_two=duel[0].player_one)
            duel.update(open=False)
            edit_duel(update_duel)
    else:
        if duel[0].duelNumber % 2 == 1 or duel[0].duelNumber == 1:
            number = int(math.ceil(duel[0].duelNumber / 2))
            update_duel = player_in_bracket(number, duel)
            update_duel.update(player_one=duel[0].player_two)
            duel.update(open=False)
            edit_duel(update_duel)
        else:
            number = int(duel[0].duelNumber / 2)
            update_duel = player_in_bracket(number, duel)
            update_duel.update(player_two=duel[0].player_two)
            duel.update(open=False)
            edit_duel(update_duel)


def number_of_rounds(round_number, bracket_size):
    while round_number != 0:
        bracket_size.append(round_number)
        round_number = int(round_number / 2)
    return bracket_size


def edit_duel(update_duel):
    if update_duel:
        if update_duel[0].player_one and update_duel[0].player_two:
            update_duel.update(open=True)


def number_of_duels(winners, duels):
    for duel in duels:
        score = Winner.objects.filter(duel=duel)
        if score:
            winners.append(score[0])
    return winners


def player_in_bracket(number, duel):
    update_duel = MatchPair.objects.filter(duelNumber=number, stage=int(duel[0].stage / 2),
                                           tournament=duel[0].tournament.id)
    return update_duel
