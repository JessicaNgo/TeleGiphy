from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import random
from .models import Game
from .giphy import gif_translate
# Create your views here.

def index(request):
    return render(request, 'game/index.html')

def new_game(request):
    token = str(random.randint(1000,9999)) #make tokens unique?
    
    #make new game in database with token
    g = Game(token = token) 
    g.save()
    
    return HttpResponseRedirect(reverse('game:waiting_lobby', args = (token,)))

def waiting_lobby(request, token):
    return render(request, 'game/wait.html', {"token": token})

def start_game(request, token):
    # current_game = get_object_or_404(Game, token)
    current_game = Game.objects.get(token=token)
    current_game.game_active = True
    current_game.save()
    
    return HttpResponseRedirect(reverse('game:game_lobby', args = (token,)))

def hotseat_gameplay(request, token):
    #if roundnumber of game is 1 (first turn)
    g = Game.objects.get(token=token)
    if g.current_round is 0:
        g.current_round += 1
        g.save()
        return render(request, 'game/hotseat_first_player.html', {'game':g} )
    else: 
        g.current_round += 1
        g.save()
        return render(request, 'game/hotseat_gameplay.html', {'game':g} )
        
def choose_new_gif(request, token):        
    return render(request, 'game/hotseat_gameplay.html')

def pass_on(request, token):
    return render(request, 'game/hotseat_gameplay.html')
# g.gameround_set.create(round_number = 1,
#                         user_text = 'hello',
#                         giphy_url = 'https://slack-imgs.com/?c=1&o1=wi320.he240&url=http%3A%2F%2Fmedia3.giphy.com%2Fmedia%2FUX1fquhNEQsLK%2Fgiphy.gif',
#                         )    
# g.save()                
    
# q = Game.objects.get(token="1234")
# derp = GameRounds(game = q, round_number = 0 , user_text = '2312', giphy_url = 'www.google.ca')
#or
# q.gamerounds_set.create(round_number etc)

# def choose_new_gif(request, token):
# / index
# new game => /new_game => generate token and redirect to waiting lobby
# /waiting_lobby/<token>

