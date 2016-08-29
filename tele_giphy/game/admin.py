# Django
from django.contrib import admin

# Localfolder
from .models import Game, GameRound, UserGame

# Register your models here.
admin.site.register(Game)
admin.site.register(UserGame)
admin.site.register(GameRound)
