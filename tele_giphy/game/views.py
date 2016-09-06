# Standard Library
import json
import random
from uuid import uuid4

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, logout as django_logout
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.models import User

# Localfolder
from .giphy import gif_random
# from .models import HOTSEAT_MODE, MULTIPLAYER_MODE, Game, GifChainStarter, GifChainNode, UserGame 
from .models import (
    HOTSEAT_MODE, MULTIPLAYER_MODE, Game, GameOverRecords, UserGame, GameRound
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


# This is where players come to wait until the game can start
def pre_game_room(request, token):
    users = User.objects.filter(usergame__game__token=token)
    return render(request, 'game/pre_game_room.html', {
        "token": token, "users": users})


def start_game(request, token):
    """
    The game is initiated through this view, not actually displayed though
    """
    # current_game can use refactoring to be queryset for easier updating and cleaner code
    current_game = Game.objects.get(token=token)
    current_game.game_active = True
    current_game.save()

    if request.session['game_mode'] == HOTSEAT_MODE:
        return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))
    elif request.session['game_mode'] == MULTIPLAYER_MODE:
        # initiallizes round 1 for all users in a multiplayer game
        users = User.objects.filter(usergame__game__token=token)
        for user in users:
            # UserGame.objects.create(
            #     user=user,
            #     game=current_game
            # )
            GameRound.objects.update_or_create(
                round_number=1,
                user=user,
                game=current_game,
                origin_user=user)
        current_game.total_rounds = len(users)
        current_game.mode = MULTIPLAYER_MODE
        current_game.save()
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


# Gets context of previous and current player actions for Hotseat Gameplay
def gameplay_context(game, token):
    if game.current_round > 1:
        # gif from last player
        received_gif = game.gameround_set.get(round_number=game.current_round - 1).giphy_url
    else:
        # if roundnumber of game is 1 (first turn)
        received_gif = ""
    try:
        game_round = game.gameround_set.get(round_number=game.current_round)
        gif = game_round.giphy_url
        phrase = game_round.user_text
    # no phrase has been entered by the player yet
    except:
        gif = static('img/giphy_static.gif')
        phrase = ""

    context = {
        'token': token,
        'game': game,
        'gif': gif,
        'phrase': phrase,
        'received_gif': received_gif
    }
    return context


# ================== HOTSEAT GAMEPLAY =========================

def hotseat_gameplay(request, token):
    g = Game.objects.get(token=token)
    context = gameplay_context(g, token)
    return render(request, 'game/hotseat_gameplay.html', context)


def choose_new_gif(request, token):
    # Default url to redirect to is for Hotseat mode
    lobby_url = 'game:game_lobby'
    if request.session['game_mode'] == MULTIPLAYER_MODE:
        lobby_url = 'game:multi_game_lobby'

    print (lobby_url)
    # Use Giphy API to retrieve a gif for the phrase entered by the user    
    response = gif_random(tag=request.POST['phrase'])
    try:
        gif = response.json()['data']['image_url']
    # If a 'bad' response is retrieved, an error should pop-up otherwise we continue
    except TypeError:
        messages.error(request, 'The phrase you entered could not produce a gif, please try something different.')
        return HttpResponseRedirect(reverse(lobby_url, args=(token,)))

    g = Game.objects.get(token=token)
    # origin_user= request.POST.get('origin_user') 
    #print(type(request.POST['origin_user']))
    print(request.POST['origin_user'] == None)
    print(request.POST['origin_user'])
    print(request.POST)
    #origin_user=1
    #origin_user= User.objects.get(username=request.POST['origin_user'])

    # If there is already a gif, update, otherwise get new gif

    update_set, game_updated = g.gameround_set.update_or_create(
        round_number=g.current_round,
        user=request.user,
        origin_user=User.objects.get(username=request.POST['origin_user']),
        defaults={
            'giphy_url': gif,
            'user_text': request.POST['phrase']})

    return HttpResponseRedirect(reverse(lobby_url, args=(token,)))


def pass_on(request, token):
    g = Game.objects.get(token=token)
    g.current_round += 1
    g.save()
    if g.mode == 'hotseat':
        return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))
    elif g.current_round > g.total_rounds:
        return HttpResponseRedirect(reverse('game:gameover', args=(token,))) #gameover_
    elif g.mode == 'multiplayer':
        return HttpResponseRedirect(reverse('game:waiting_room', args=(token,)))


# ================== MULTIPLAYER GAMEPLAY =========================

def _is_player_turn(request, user):
    pass


def multi_gameplay(request, token):
# Each request recognizes which player is making the request due to session cookies
    # You can test this by having private browser windows and logging in as other players
# This should mimic 1 round of hotseat and store info as the request user in the model
# After a player passes/commits to gif, they go to waiting
# Waiting redirects to game_lobby when all players have gone 
    game = Game.objects.get(token=token)
    print(game.current_round)

    # Game rounds corresponding to all players in this multiplayer game
    if game.current_round > 1:
        previous_round = game.current_round - 1 
    else:
        previous_round = game.current_round
    game_rounds = game.gameround_set.filter(round_number=previous_round)

    # Determine the "placement" of current user and the user "before"
    ordered_users = User.objects.filter(usergame__game__token=token).order_by('username')

    for user_index, user in enumerate(ordered_users):
        if user == request.user:
            request_user_index = user_index
            try:
                previous_user_index = user_index - 1
                previous_user = ordered_users[previous_user_index]
            except AssertionError:
                # First player with index of 0
                previous_user_index = len(ordered_users) - 1
                previous_user = ordered_users[previous_user_index]
            break

    # Find game round requesting user is suppose to act on
    previous_game_round = game_rounds.get(
        user=previous_user, round_number=previous_round)

    # Build context
    if game.current_round > 1:
        # gif and origin_user from last player
        received_gif = previous_game_round.giphy_url
        origin_user = previous_game_round.origin_user
    else:
        # if roundnumber of game is 1 (first turn)
        received_gif = ""
        origin_user = request.user
    
    try:
        game_round = game.gameround_set.get(
            round_number=game.current_round, 
            user=request.user)
        gif = game_round.giphy_url
        phrase = game_round.user_text
    # no phrase has been entered by the player yet
    except:
        gif = static('img/giphy_static.gif')
        phrase = ""
        game.gameround_set.get_or_create(
            round_number=game.current_round,
            user=request.user,
            origin_user=origin_user
            )

    context = {
        'token': token,
        'game': game,
        'gif': gif,
        'phrase': phrase,
        'received_gif': received_gif,
        'origin_user': origin_user
    }

    return render(request, 'game/multi_gameplay.html', context)


def waiting_room(request, token):
    # logic to check to see if all players are ready
    game = Game.objects.get(token=token)
    game_rounds = game.gameround_set.filter(round_number=game.current_round)
    print(game.current_round)
    print(game_rounds.count())
    print(game.total_rounds)

    if game_rounds.count() == game.total_rounds:
        print("init")
        return HttpResponseRedirect(reverse('game:multi_game_lobby', args=(token,)))
    return render(request, 'game/multi_waiting_room.html')


def gameover_waiting_room(request, token):
    return render(request, 'game/multi_waiting_room.html')

# ================== GAMEOVER =========================

def gameover(request, token):
    # Checks what kind of token is passed and fetch object
    # End of game token
    if len(token) == 4:
        # Check if gameover already happened, if so display postGameToken
        try:
            gameover = GameOverRecords.objects.get(game_token=token)
            # If game ended before actions were made
            if len(gameover.records) == 2:
                return render(request, 'game/gameover.html', {
                    "result": "Game ended without any rounds",
                    "doge": gif_random('doge').json()['data']['image_url']})
            # If game ended with actions
            result_url = reverse('game:gameover', args=(gameover.token,))
            return render(request, 'game/gameover.html', {
                "result": '',
                "token": gameover.token,
                "request_url": result_url})
        # Game has not ended
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
        all_origin_users = set([gRound.origin_user.username for gRound in game_rounds])
        result = {name: {'rounds': []} for name in all_origin_users}

        # Populate dict for gameover display and record storage
        for gTurn in game_rounds:
            if gTurn.user_text == '':
                user_text = '[BLANK]'
            else:
                user_text = gTurn.user_text
            result[gTurn.origin_user.username]['rounds'].append(
                {'user_text': user_text,
                 'giphy_url': gTurn.giphy_url})

        print(result)
        # Stores a json of all players actions in post-gameover model
        postGameToken = str(uuid4())
        result_json = json.dumps(result)
        GameOverRecords.objects.create(
            token=postGameToken,
            records=result_json,
            game_token=g.token,
            mode=game_mode)

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

    # If game ended before actions were made
    if len(result) < 1:
        return render(request, 'game/gameover.html', {
            "result": "Game ended without any rounds",
            "doge": gif_random('doge').json()['data']['image_url']})

    # Gameover screen
    return render(request, 'game/gameover.html', {
        "result": result,
        "token": postGameToken,
        "game_mode": game_mode})
