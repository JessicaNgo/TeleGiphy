# Django
from django.contrib.auth.models import User
from django.db import models

MULTIPLAYER_MODE = "multiplayer"
HOTSEAT_MODE = "hotseat"


# Keeps tabs on a game token, whether game has started, and ended
class Game(models.Model):
    token = models.CharField(max_length=16)
    game_active = models.BooleanField(default='False')
    game_over = models.BooleanField(default='False')
    current_round = models.IntegerField(default=1)
    mode = models.CharField(max_length=20, default=HOTSEAT_MODE)

    def __str__(self):
        return self.token


# Keeps track of what game is attached to a user
class UserGame(models.Model):
    '''
    USER --- USERGAME --\
    USER --- USERGAME --- GAME
    USER --- USERGAME --/
    '''
    user = models.OneToOneField(User)
    game = models.ForeignKey(Game)
    
    def __str__(self):
        return self.user.username

    # token can be added if there are persistent users
    # token = models.CharField(max_length=16)

    # def __str__(self):
    #     return str(self.username)


# Keeps track of game rounds
class GameRound(models.Model):
    round_number = models.IntegerField()
    user_text = models.CharField(max_length=150)
    giphy_url = models.CharField(max_length=2083)  # 2083 is max of URL length
    user = models.ForeignKey(User, related_name='gameround_user')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    origin_user = models.ForeignKey(UserGame, on_delete=models.CASCADE, related_name='origin_user', null=True)
