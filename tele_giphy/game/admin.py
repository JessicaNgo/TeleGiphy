# Django
from django.contrib import admin

# Localfolder
from .models import Game, GameRound, UserGame

# Text Form widget
from charsleft_widget.widgets import CharsLeftInput, MediaMixin
from django.db import models
# The MediaMixin is what loads the css and javascript only one time per admin page
class TextModelAdmin(MediaMixin, admin.ModelAdmin):
  # Use widget on all instances of this form field
  formfield_overrides = {
    models.CharField: {'widget': CharsLeftInput()},
  }


# Register your models here.
admin.site.register(Game, TextModelAdmin)
admin.site.register(UserGame, TextModelAdmin)
admin.site.register(GameRound, TextModelAdmin)
