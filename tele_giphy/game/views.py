from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import random
from .models import Game
from .giphy import gif_random
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
    
    try:
            # g.gameround_set.get(round_number=g.current_round)
            gif = g.gameround_set.get(round_number = g.current_round).giphy_url
    except:
            gif = "http://media0.giphy.com/media/YJBNjrvG5Ctmo/giphy.gif"
    
    context = {
        'token': token, 
        'game':g, 
        'gif':gif
        }
    if g.current_round is 1:
        
        return render(request, 'game/hotseat_first_player.html', context )
    else:
        return render(request, 'game/hotseat_gameplay.html', context)
        
def choose_new_gif(request, token):
    
    response = gif_random(tag = request.POST['phrase'] )
    gif = response['data']['image_url']
    
    g = Game.objects.get(token=token)
    try:
        g_round = g.gameround_set.get(round_number = g.current_round)
        g_round.user_text = request.POST['phrase']
        g_round.giphy_url = gif
        g_round.save()
    except:
        g.gameround_set.create( round_number = g.current_round, 
                            user_text = request.POST['phrase'],
                            giphy_url = gif)
        g.save()                
    
    return HttpResponseRedirect(reverse('game:game_lobby', args = (token,)))

def pass_on(request, token):
    
    g = Game.objects.get(token=token)
    g.current_round += 1
    g.save()
    
    return HttpResponseRedirect(reverse('game:game_lobby', args = (token,)))
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

