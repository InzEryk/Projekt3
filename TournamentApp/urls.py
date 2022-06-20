from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('tournament', views.all_tournaments, name="tournament_list"),
    path('show_tournament/<tournament_id>', views.show_tournament, name='show_tournament'),
    path('add_tournament', views.add_tournament, name='add_tournament'),
    path('add_tournament/<tournament_id>/', views.add_players, name='add_players'),
    path('tournament_restricted', views.tournament_restricted, name='tournament_list_restricted'),
    path('edit_tournament/<tournament_id>', views.edit_tournament, name='edit_tournament'),
    path('delete_tournament/<tournament_id>', views.delete_tournament, name='delete_tournament'),
    path('bracket/<tournament_id>/', views.bracket_tournament, name='bracket'),
    path('edit_bracket/<tournament_id>', views.edit_bracket_tournament, name='edit_bracket'),
    path('score/<int:id>/', views.duel_winner, name='score'),
    path('history', views.history, name='history'),
    path('open_close', views.open_close, name='open_close'),
    path('show_history/<tournament_id>', views.show_history, name='show_history'),

]

