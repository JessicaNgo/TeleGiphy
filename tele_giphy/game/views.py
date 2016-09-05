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
from django.contrib.staticfiles.templatetags.staticfiles import static

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
    current_game = Game.objects.get(token=token)
    current_game.game_active = True
    current_game.save()

    if request.session['game_mode'] == HOTSEAT_MODE:
        return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))
    else:
        # initiallizes round 1 for all users in a multiplayer game
        users = User.objects.filter(usergame__game__token=token)
        for user in users:
            GameRound.objects.create(
                round_number=1,
                user=user.user,
                game=current_game,
                origin_user=user.user)
        current_game.total_rounds = len(users)
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
        game_round = g.gameround_set.get(round_number=g.current_round)
        gif = game_round.giphy_url
        phrase = game_round.user_text
        context = {
            'token': token,
            'game': g,
            'gif': gif,
            'phrase': phrase,
            'received_gif': received_gif
        }
    # no phrase has been entered by the user yet
    except:
        gif = static('img/giphy_static.gif')
        context = {
            'token': token,
            'game': g,
            'gif': gif,
            'received_gif': received_gif
        }
    return render(request, 'game/hotseat_gameplay.html', context)


def choose_new_gif(request, token):
    response = gif_random(tag=request.POST['phrase'])
    try:
        gif = response.json()['data']['image_url']
    except TypeError:
        messages.error(request, 'The phrase you entered could not produce a gif, please try something different.')
        return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))

    g = Game.objects.get(token=token)

    # If there is already a gif, update, otherwise get new gif
    g.gameround_set.update_or_create(
        round_number=g.current_round,
        user_text=request.POST['phrase'],
        user=request.user,
        defaults={'giphy_url': gif})

    return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))


def pass_on(request, token):
    g = Game.objects.get(token=token)
    g.current_round += 1
    g.save()
    if g.current_round > g.total_rounds:
        return HttpResponseRedirect(reverse('game:gameover_waiting_room', args=(token,)))
    elif g.mode == 'hotseat':
        return HttpResponseRedirect(reverse('game:game_lobby', args=(token,)))
    elif g.mode == 'multiplayer':
        return HttpResponseRedirect(reverse('game:waiting_room', args=(token,)))


# ================== MULTIPLAYER GAMEPLAY =========================

def _is_player_turn(request, user):
    pass


def multi_gameplay(request, token):
    game = Game.objects.get(token=token)
    users = User.objects.filter(usergame__game__token=token)
    temp_user_list = [user.username for user in users if user.username]
    request.session['other_user_origins'] = dict(enumerate(temp_user_list, start=2))
    request.session['player_round'] = 1  # increment each time local player passes on gif
    context = {
        'token': token,
        'game':game
    }
    
    max_rounds = users.count()
    
    if game.current_round == 1:
        game_round = game.gameround_set.filter(origin_user=request.user)
    elif game.current_round <= max_rounds:
        current_player_round = session['player_round']
        # next_user_origin = request.session['other_user_origins'][current_player_round].
        # previous_game_round = game.gameround_set.filter(origin_user=next_user_origin, round_number = session[])
    #TODO:     
    #having trouble determining player order
    gif = game_round.giphy_url
    phrase = game_round.user_text
    
    try:
        context['gif'] = gif
        context['phrase'] = phrase
    except:
        pass
    # context = {
    #         'token': token,
    #         'game': g,
    #         'gif': gif,
    #         'phrase': phrase,
    #         'received_gif': received_gif
    #     }
    #display recieved gif #display phrase #display gif
    
    # check if it is the players turn, if not, show a waiting for turn page, or anythingn really
#     #if it is the players turn, let them enter a phrase/guess, same as hotseat
#     #After passing on, redirect to results page, (results page will show nothing until final player goes_
#     #if the final player has entered the gif, results page will be displayed
#     #include a button on results page to refresh
        raise NotImplemented("Hello")


def waiting_room(request, token):
    pass


def gameover_waiting_room(request, token):
    pass

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


###remove code below when gameplay is done, for reference
#code is the incomplete linkedlist implementation
# def multi_gameplay(request, token):
#     #TO DO: determine player sequence
#     game = Game.objects.get(token=token)
#     users = User.objects.filter(usergame__game__token=token)
    
#     temp_user_list = [user.username for user in users if user.username != request.user]
#     request.session['user_sequence'] = dict(enumerate(temp_user_list, start=1))
    
#     max_rounds = users.count()
    
#     if game.current_round <= max_rounds:
        
#         context = {
#                 'token': token,
#                 'game': game
#                 }
        
#         if game.current_round == 1:
#             first_player_node = GifChainStarter.objects.get(user=request.user).first_node
#             gif = first_player_node.giphy_url
#             phrase = first_player_node.user_text
#         else:
#             chain_owner_username = request.session['user_sequence'][(game.current_round)]
#             chain_owner_user_object = User.objects.get(username = chain_owner_username)
#             starter_chain = GifChainStarter.objects.get(user=chain_owner_user_object)
#             last_node = starter_chain.get_last_node
#             received_gif = last_node.giphy_url
#             context['received_gif'] = received_gif
#             # phrase = last_node.user_text
        
#         try:
#             context['gif'] = last_node.next_node.giphy_url
#             context['phrase'] = last_node.next_node.user_text
#         except:
#             pass

#         return render(request, 'game/multi_gameplay.html', context)
#     else:
#         #end da game
#         return render(request, 'game/multi_results.html')
#     # users = game.usergame_set.users.all()
#     '''
    
#     GifChainStarter ----- GIFCHAIN(USER) ----- GIFCHAIN(USER) ---- GIFCHAIN
#       user
#       order (in sequence of players)
#       gif
#       game
#     '''
#     #check if it is the players turn, if not, show a waiting for turn page, or anythingn really
#     #if it is the players turn, let them enter a phrase/guess, same as hotseat
#     #After passing on, redirect to results page, (results page will show nothing until final player goes_
#     #if the final player has entered the gif, results page will be displayed
#     #include a button on results page to refresh
#     raise NotImplementedError("Hello")
    
# def multi_choose_new_gif(request, token):
    
#     raise NotImplementedError("Hello")


# def multi_pass_on(request, token):
#     chain_owner_username = request.session['user_sequence'][(game.current_round)]
#     chain_owner_user_object = User.objects.get(username = chain_owner_username)
#     starter_chain = GifChainStarter.objects.get(user=chain_owner_user_object)
#     last_node = starter_chain.get_last_node
#     game.current_round = game.current_round + 1
#     game.save() 
    
#     last_node.next_node = GifChainNode.objects.create(user = request.user)
#     raise NotImplementedError("Hello")
