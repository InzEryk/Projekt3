from django.db import models
from django.core.validators import MinValueValidator


SIZE_BOARDS= (
    (4, 4),
    (8, 8),
    (16, 16),
    (32, 32),
    (64, 64),
)


class Tournament(models.Model):
    name = models.CharField(max_length=100, default='')
    started_date = models.DateTimeField()
    number_of_players = models.IntegerField(choices=SIZE_BOARDS)
    owner = models.IntegerField(blank=False, default=1)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Player(models.Model):
    name = models.CharField(max_length=100, default='')
    tournament = models.ForeignKey(Tournament,
                                   on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.name}"


class MatchPair(models.Model):
    player_one = models.ForeignKey(Player,
                                   related_name='player_one',
                                   on_delete=models.CASCADE, default='', null=True)
    player_two = models.ForeignKey(Player,
                                   on_delete=models.CASCADE,
                                   related_name='player_two', default='', null=True)
    tournament = models.ForeignKey(Tournament, related_name='tournament', on_delete=models.CASCADE)
    duelNumber = models.IntegerField(null=False, default='')
    stage = models.IntegerField(null=False, default='')
    open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.player_one} {self.player_two} {self.tournament} {self.duelNumber} {self.stage}"


class Winner(models.Model):
    duel = models.ForeignKey(MatchPair, on_delete=models.CASCADE, null=False)
    player_one_score = models.IntegerField(null=False, validators=[MinValueValidator(0)], default=0)
    player_two_score = models.IntegerField(null=False, validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.duel} {self.player_one_score} {self.player_two_score}"
