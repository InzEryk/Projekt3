from django.contrib import admin
from .models import Player, Tournament, MatchPair, Winner, History

admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(MatchPair)
admin.site.register(Winner)
admin.site.register(History)
