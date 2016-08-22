from django.contrib import admin
from .models import Game, User, GameRound
# Register your models here.
admin.site.register(Game)
admin.site.register(User)
admin.site.register(GameRound)