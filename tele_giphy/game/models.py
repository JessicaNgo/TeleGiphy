from django.db import models

# Keeps tabs on a game token, whether game has started, and ended
class Game(models.Model):
    # def __str__(self):
    #     return {'gametoken'}
    token = models.CharField(max_length=16)
    game_active = models.BooleanField(default='False')
    game_over = models.BooleanField(default='False')
    current_round = models.IntegerField(default = 0)
    def __str__(self):
        return self.token

# Keeps track of users in relation to game tokens
class User(models.Model):
    username = models.CharField(max_length=60)
    # token = models.CharField(max_length=16)
    
    def __str__(self):
        return str(self.username)

# Keeps track of game rounds
class GameRound(models.Model):
    round_number = models.IntegerField()
    user_text = models.CharField(max_length=150)
    giphy_url = models.CharField(max_length=2083) #Should be the AWS S3 URL, uses limitation of URL length
    # user = models.ForeignKey(User, on_delete=models.CASCADE) #many to many relationship instead of many to one relationship?
    game = models.ForeignKey(Game, on_delete=models.CASCADE) #many game rounds related to one game


# q = Game.objects.get(token="1234")
# derp = GameRounds(game = q, round_number = 0 , user_text = '2312', giphy_url = 'www.google.ca')
#or
# q.gamerounds_set.create(round_number etc)