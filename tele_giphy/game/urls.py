# Django
from django.conf.urls import url

# Localfolder
from . import views

app_name = 'game'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_game$', views.new_game, name='new_game'),
    url(r'^join_game$', views.join_game, name='join_game'),
    url(r'^pre_game_room/(?P<token>[0-9]+)/$', views.pre_game_room, name='pre_game_room'),
    url(r'^pre_game_room/(?P<token>[0-9]+)/start_game$', views.start_game, name='start_game'),
    url(r'^game_lobby/(?P<token>[0-9]+)/$', views.hotseat_gameplay, name='game_lobby'),
    url(r'^game_lobby/(?P<token>[0-9]+)/choose_new_gif$', views.choose_new_gif, name='choose_new_gif'),
    url(r'^game_lobby/(?P<token>[0-9]+)/next$', views.pass_on, name='pass_on'),
    url(r'^gameover/(?P<token>[\w\-]+)/$', views.gameover, name='gameover'),
    url(r'^multi_game_lobby/(?P<token>[0-9]+)/$', views.multi_gameplay, name='multi_game_lobby'),
    url(r'^waiting_room/(?P<token>[0-9]+)/$', views.waiting_room, name='waiting_room'),
    url(r'^choose_name', views.choose_name, name='choose_name')
]
