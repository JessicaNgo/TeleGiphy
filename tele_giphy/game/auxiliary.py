from uuid import uuid4

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.urls import reverse

from .models import (
    HOTSEAT_MODE, MULTIPLAYER_MODE, Game, GameOverRecords, UserGame, GameRound
)

def _give_random_name(request):
    user = User.objects.create(username=str(uuid4()))
    _login_user(request, user)
    messages.info(request, 'Your name has randomly been set to {}.'.format(user.username))

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