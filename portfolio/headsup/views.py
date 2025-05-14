from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    players = Player.objects.all()
    matches = Match.objects.all()
    return render(request, 'index.html', {
        'players':players,
        'matches':matches,
        })

def list_matches(request):
    matches = Match.objects.all().order_by("-date")
    return render(request, 'match/match_list.html', {
        'matches':matches,
    })

def create_match(request):
    errors = []
    players = Player.objects.all()
    if request.method == 'POST':
        player_1_id = request.POST.get('player_1')
        player_2_id = request.POST.get('player_2')
        serving_first = request.POST.get('serving_first')
        format = request.POST.get('format')
        location = request.POST.get('location')
        tournament = request.POST.get('tournament')
        date = request.POST.get('date')

        # Validate
        if not player_1_id:
            errors.append("Please enter a Player 1.")
        if not player_2_id:
            errors.append("Please enter a Player 2.")
        if player_1_id and player_2_id and player_1_id == player_2_id:
            errors.append("Player 1 and Player 2 cannot be the same player.")
        if not serving_first:
            errors.append("Please select who will be serving first.")
        if not format:
            errors.append("Please add a Match format.")
        elif format not in dict(FORMAT_CHOICES):  
            errors.append("Please add a valid Match format.")
        if not location:
            errors.append("Please add a Match location")
        if not tournament:
            errors.append("Please add a Tournament/Competition")
        if not date:
            errors.append("Please add a date")

        if not errors:
            try:
                player_1 = Player.objects.get(id=player_1_id)
                player_2 = Player.objects.get(id=player_2_id)
            except Player.DoesNotExist:
                errors.append("One of the players does not exist.")
            else:
                match = Match(format=format, location=location, tournament=tournament, date=date)
                match.serving_first = player_1 if serving_first == 'player_1' else player_2
                match.save()
                match.players.add(player_1, player_2)
                return redirect('index')


    return render(request, 'match/match_create.html', {
        'players': players,
        'format_choices': FORMAT_CHOICES,
        'errors': errors,
    })

def view_match(request, match_id):
    match = Match.objects.get(id=match_id)
    players = list(match.players.all())  
    return render(request, 'match/match_view.html', {
        "match": match,
        "players": players,
    })

def list_players(request):
    players = Player.objects.all()
    return render(request, 'player/player_list.html', {
        'players':players,
    })

def create_player(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        handedness = request.POST['handedness']
        fh_handedness = request.POST['fh_handedness']
        bh_handedness = request.POST['bh_handedness']
        
        # Need to add validation to this form: 
        newPlayer = Player(
            first_name=first_name,
            last_name=last_name,
            handedness=handedness,
            fh_handedness=fh_handedness,
            bh_handedness=bh_handedness,
        )

        newPlayer.save()
        return redirect('index')
    else:
        return render(request, 'player/player_create.html')

def view_player(request, player_id):
    player = Player.objects.get(id=player_id)
    matches = player.matches_played.all().order_by("-date")
    return render(request, 'player/player_view.html', {
        "player": player,
        "matches": matches,
    })
    
def view_game(request, match_id):
    match = Match.objects.get(id=match_id)
    players = list(match.players.all())  
    serving = 0 if match.serving_first == match.players.all()[0] else 1
    receiving = 1 - serving
    return render(request, 'game/game_view.html', {
        "match": match,
        "players": players,
        "serving": serving,
        "receiving": receiving,
    })
