# Django
from django.db import models


# Keeps tabs on a game token, whether game has started, and ended
class Game(models.Model):
    token = models.CharField(max_length=16)
    game_active = models.BooleanField(default='False')
    game_over = models.BooleanField(default='False')
    current_round = models.IntegerField(default=1)

    def __str__(self):
        return self.token


# Keeps track of users in relation to game tokens
class User(models.Model):
    username = models.CharField(max_length=60)

    # token can be added if there are persistent users
    # token = models.CharField(max_length=16)

    def __str__(self):
        return str(self.username)


# Keeps track of game rounds
class GameRound(models.Model):
    round_number = models.IntegerField()
    user_text = models.CharField(max_length=150)
    giphy_url = models.CharField(max_length=2083)  # 2083 is max of URL length
    user = models.ManyToManyField(User, related_name='user')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    origin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='origin_user', null=True)
