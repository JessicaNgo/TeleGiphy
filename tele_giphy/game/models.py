from django.db import models

# Keeps tabs on a game token, whether game has started, and ended
class Game(models.Model):
    token = models.CharField(max_length=16)
    game_active = models.BooleanField(default='False')
    game_over = models.BooleanField(default='False')

# Keeps track of users in relation to game tokens
class User(models.Model):
    username = models.CharField(max_length=60)
    token = models.CharField(max_length=16)

# Keeps track of game rounds
class GameRounds(models.Model):
    round_number = models.IntegerField()
    user_text = models.CharField(max_length=150)
    giphy_url = models.CharField(max_length=2083) #Should be the AWS S3 URL, uses limitation of URL length
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_token = models.ForeignKey(GameToken, on_delete=models.CASCADE)

