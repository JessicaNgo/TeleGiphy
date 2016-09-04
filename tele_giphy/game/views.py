# Standard Library
import json
import random
from uuid import uuid4

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, logout as django_logout
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

# Localfolder
from .giphy import gif_random
from .models import (
    HOTSEAT_MODE, MULTIPLAYER_MODE, Game, GameOverRecords, UserGame,
)

User = get_user_model()


def index(request):
    """
    This is the index view. That is all.
    """
    return render(request, 'game/index.html')


def _give_random_name(request):
    user = User.objects.create(username=str(uuid4()))
    _login_user(request, user)
    messages.info(request, 'Your name has randomly been set to {}.'.format(user.username))


def new_game(request):
    """
    This view creates a new game token when a user clicks on "New Game" button on index.html
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
    request.session['game_mode'] = request.POST['game_mode']
    game = Game(token=new_token, mode=request.session['game_mode'])
    game.save()
    if not request.user.is_authenticated():
        _give_random_name(request)

    try:
        _attach_user_to_game(game, request)
    except IntegrityError:
        return redirect(reverse('game:index'))
    return HttpResponseRedirect(reverse('game:pre_game_room', args=(new_token,)))


def _attach_user_to_game(game, request):
    try:
        UserGame.objects.get(user=request.user)
        url = reverse('game:pre_game_room', args=(request.user.usergame.game,))
        messages.error(request,
                       'You are already part of a game ({token}). <a href="{url}">Click here to join it.</a>'.format(
                           token=request.user.usergame.game, url=url))
        raise IntegrityError
    except UserGame.DoesNotExist:
        UserGame.objects.create(user=request.user, game=game)


def _delete_game(game):
    g = Game.objects.get(game=game)
    g.delete()


def join_game(request):
    """
    This view allows a different users to join a pre-exisiting game if it exists.
    If it exists, it should also check to see if the user is still able to join the game.
    """
    token = request.POST["join_token"]
    try:
        game = Game.objects.get(token=token)
        if not game.mode == MULTIPLAYER_MODE:
            messages.error(request, 'Not a multiplayer game.')
        elif game.game_active or game.game_over:
            messages.error(request, 'Cannot join that game, it has already started or ended.')
        else:
            if not request.user.is_authenticated():
                _give_random_name(request)
            try:
                _attach_user_to_game(game, request)
            except IntegrityError:
                return redirect(reverse('game:index'))
            request.session['game_mode'] = MULTIPLAYER_MODE
            return redirect(reverse('game:pre_game_room', args=(token,)))
    except Game.DoesNotExist:
        messages.error(request, 'Game not found.')

    return redirect(reverse('game:index'))


def pre_game_room(request, token):
    """
    This is where players come to wait until the game can start
    """
    users = User.objects.filter(usergame__game__token=token)
    return render(request, 'game/pre_game_room.html', {"token": token, "users": users})


def start_game(request, token):
    """
    The game is initiated through this view, not actually displayed though
    """
    current_game = Game.objects.get(token=token)
    current_game.game_active = True
    current_game.save()

    if request.session['game_mode'] == HOTSEAT_MODE:
        return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))
    else:
        return HttpResponseRedirect(reverse('game:multi_game_lobby', args=(token,)))


def _login_user(request, user):
    """
    Log in a user without requiring credentials (using ``login`` from
    ``django.contrib.auth``, first finding a matching backend).

    """
    from django.contrib.auth import load_backend, login
    if not hasattr(user, 'backend'):
        for backend in settings.AUTHENTICATION_BACKENDS:
            if user == load_backend(backend).get_user(user.pk):
                user.backend = backend
                break
    if hasattr(user, 'backend'):
        return login(request, user)


def choose_name(request):
    username = request.POST['username']
    try:
        user = User.objects.create(username=username)
        if request.user.is_authenticated():
            old_user = request.user
            django_logout(request)
            old_user.delete()
        _login_user(request, user)
        messages.success(request, 'You have chosen "{}"!'.format(username))
    except IntegrityError:
        messages.error(request, 'Sorry, "{}" is already taken :('.format(username))

    return redirect(request.GET.get('next', '/'))


# ================== HOTSEAT GAMEPLAY =========================
def hotseat_gameplay(request, token):
    # if roundnumber of game is 1 (first turn)
    g = Game.objects.get(token=token)
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
# def select_phrase(request, token):
#     phrase = request.POST['phrase']


def choose_new_gif(request, token):
    response = gif_random(tag=request.POST['phrase'])
    try:
        gif = response.json()['data']['image_url']
    except TypeError:
        messages.error(request, 'The phrase you entered could not produce a gif, please try something different.')
        return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))

    g = Game.objects.get(token=token)

    # If there is already a gif, update, otherwise get new gif
    g, g_round = g.gameround_set.update_or_create(
        round_number=g.current_round,
        user_text=request.POST['phrase'],
        user=request.user,
        defaults={'giphy_url': gif})

    return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))


def pass_on(request, token):
    g = Game.objects.get(token=token)
    # print(g.current_round)
    g.current_round += 1
    # print(g.current_round)
    g.save()

    return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))


# def _login_user(request, user):

#     Log in a user without requiring credentials (using ``login`` from
#     ``django.contrib.auth``, first finding a matching backend).
# =======

# ================== MULTIPLAYER GAMEPLAY =========================

def multi_gameplay(request, token):
    # first lets only work on one game at a time
    # TO DO:
    # check if it is the players turn, if not, show a waiting for turn page, or anythingn really
    # if it is the players turn, let them enter a phrase/guess, same as hotseat
    # After passing on, redirect to results page, (results page will show nothing until final player goes_
    # if the final player has entered the gif, results page will be displayed
    # include a button on results page to refresh

    raise NotImplementedError("Hello")


def gameover(request, token): 
    # Checks what kind of token is passed and fetch object
    # End of game token
    if len(token) == 4:
        # Check if gameover already happened, if so display postGameToken
        try:
            gameover = GameOverRecords.objects.get(game_token=token)
            result_url = reverse('game:gameover', args=(gameover.token,))
            return render(request, 'game/gameover.html', {
                "result": '', 
                "token": gameover.token,
                "request_url":result_url})
        except GameOverRecords.DoesNotExist:
            g = get_object_or_404(Game, token=token)
    
    # (Maybe) gameover records token
    elif len(token) > 4:
        g = get_object_or_404(GameOverRecords, token=token) 

    # Type of game that's being played
    game_mode = g.mode

    # Processes gameRounds and stores it
    if isinstance(g, Game):
        # Fetch game round records, ordered by origin user and round number
        game_rounds = g.gameround_set.all().order_by('origin_user', 'round_number')

        # Users from game (for now), UserGame model not yet populating
        all_origin_users = set([gRound.origin_user for gRound in game_rounds])
        result = {name: {'rounds': []} for name in all_origin_users}

        # Populate dict for gameover display and record storage
        for gTurn in game_rounds:
            if gTurn.user_text == '':
                user_text = '[BLANK]'
            else:
                user_text = gTurn.user_text
            result[gTurn.origin_user]['rounds'].append(
                {'user_text': user_text,
                 'giphy_url': gTurn.giphy_url})

        # Stores a json of all players actions in post-gameover model
        postGameToken = str(uuid4())
        result_json = json.dumps(result)
        GameOverRecords.objects.create(
            token = postGameToken,
            records = result_json, 
            game_token = g.token,
            mode = game_mode)

        # Signout of user session, delete user and game
        user = request.user
        django_logout(request)
        if user.is_authenticated:
            user.delete()
        g.delete()

    # Gets Previously stored gameover records
    elif isinstance(g, GameOverRecords):
        result = json.loads(g.records)
        postGameToken = g.token
    else:
        raise Http404

    return render(request, 'game/gameover.html', {
        "result": result, 
        "token": postGameToken, 
        "game_mode": game_mode})


def multi_choose_new_gif(request, token):
    raise NotImplementedError("Hello")


def multi_pass_on(request, token):
    raise NotImplementedError("Hello")
