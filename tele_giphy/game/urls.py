from django.conf.urls import url

from . import views

app_name = 'game'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_game$', views.new_game, name='new_game'),
    url(r'^join_game$', views.join_game, name='join_game'),
    url(r'^waiting_lobby/(?P<token>[0-9]+)/$', views.waiting_lobby, name='waiting_lobby'),
    url(r'^waiting_lobby/(?P<token>[0-9]+)/start_game$', views.start_game, name='start_game'),
    url(r'^game_lobby/(?P<token>[0-9]+)/$', views.hotseat_gameplay, name='game_lobby'),
    url(r'^game_lobby/(?P<token>[0-9]+)/choose_new_gif$', views.choose_new_gif, name='choose_new_gif'),
    url(r'^game_lobby/(?P<token>[0-9]+)/next$', views.pass_on, name='pass_on'),
    # url(r'^hot$', views.hot, name = 'hot'),
    # need to add view for game lobby then update line 10 with new view
]
