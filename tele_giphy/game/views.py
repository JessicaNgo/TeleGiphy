# Standard Library
import random

# Django
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Localfolder
from .giphy import gif_random
from .models import Game


# Create your views here.

def index(request):
    """ This is the index view."""
    return render(request, 'game/index.html')


def new_game(request):
    """ This view creates a new game token when a user clicks on "New Game" button on index.html
    This is done randomly and then checks in the database to see if that token is already present.
    If so, it'll keep on trying until it finds a unique token.
    """
    # Makes initial token
    new_token = str(random.randint(1000, 9999))
    # Checks to see if the token created is unique
    # What if ALL tokens already taken? Well, that would suck!
    while Game.objects.filter(token=new_token).exists():
        new_token = str(random.randint(1000, 9999))
    # Make new game in database with the token
    g = Game(token=new_token)
    g.save()
    return HttpResponseRedirect(reverse('game:waiting_lobby', args=(new_token,)))


def join_game(request):
    """ This view allows a different users to join a pre-exisiting game if it exists.
    If it exists, it should also check to see if the user is still able to join the game.
    """
    token = request.POST["join_token"]
    # Check to see if game corresponding to game token exists
    # An AND statement to check to see if the game is already "closed" should be added here
    if Game.objects.filter(token=token).exists():
        return HttpResponseRedirect(reverse('game:waiting_lobby', args=(token,)))
    messages.error(request, "Token not found or invalid.")
    return render(request, 'game/index.html', status=302)


def waiting_lobby(request, token):
    return render(request, 'game/pre_game_room.html', {"token": token})


def start_game(request, token):
    # current_game = get_object_or_404(Game, token)
    current_game = Game.objects.get(token=token)
    current_game.game_active = True
    current_game.save()

    return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))


# ==================
def hotseat_gameplay(request, token):
    # if roundnumber of game is 1 (first turn)
    g = Game.objects.get(token=token)
    if g.current_round == 4:
        print(g.gameround_set.all())
        return render(request, 'game/hotseat_results.html', {"results": g.gameround_set.all()})
    if g.current_round > 1:
        received_gif = g.gameround_set.get(round_number=g.current_round - 1).giphy_url
    else:
        received_gif = ""
    try:
        # g.gameround_set.get(round_number=g.current_round)
        gif = g.gameround_set.get(round_number=g.current_round).giphy_url
        phrase = g.gameround_set.get(round_number=g.current_round).user_text
        context = {
            'token': token,
            'game': g,
            'gif': gif,
            'phrase': phrase,
            'received_gif': received_gif
        }
    except:
        gif = "http://media0.giphy.com/media/YJBNjrvG5Ctmo/giphy.gif"
        context = {
            'token': token,
            'game': g,
            'gif': gif,
            'received_gif': received_gif
        }
    return render(request, 'game/hotseat_gameplay.html', context)


# Not sure what this is for..? \/\/\/        
def select_phrase(request, token):
    phrase = request.POST['phrase']


def choose_new_gif(request, token):
    response = gif_random(tag=request.POST['phrase'])
    gif = response.json()['data']['image_url']

    g = Game.objects.get(token=token)
    try:
        g_round = g.gameround_set.get(round_number=g.current_round)
        g_round.user_text = request.POST['phrase']
        g_round.giphy_url = gif
        g_round.save()
    except:
        g.gameround_set.create(round_number=g.current_round,
                               user_text=request.POST['phrase'],
                               giphy_url=gif)
        g.save()

    return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))


def pass_on(request, token):
    g = Game.objects.get(token=token)
    print(g.current_round)
    g.current_round += 1
    print(g.current_round)
    g.save()

    return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))
