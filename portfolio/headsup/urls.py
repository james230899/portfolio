from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    
    path('players', views.list_players, name="list_players"),
    path('create_player', views.create_player, name="create_player"),
    path('player/<int:player_id>', views.view_player, name="view_player"),

    path('matches', views.list_matches, name="list_matches"),
    path('create_match', views.create_match, name="create_match"),
    path('match/<int:match_id>', views.view_match, name="view_match"),


    path('match/<int:match_id>/view_game', views.view_game, name="view_game"),

]
