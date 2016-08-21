from django.conf.urls import url

from . import views

app_name = 'game'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_game$', views.new_game, name = 'new_game'),
    url(r'^waiting_lobby/(?P<token>[0-9]+)/$', views.wait, name='waiting_lobby'),
    url(r'^game_lobby/(?P<token>[0-9]+)/$', views.hotseat_gameplay, name = 'game_lobby')
    #need to add view for game lobby then update line 10 with new view
]
