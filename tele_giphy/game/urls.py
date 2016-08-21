from django.conf.urls import url

from . import views

app_name = 'game'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<token>[0-9]+)/$', views.wait, name='waiting_lobby'),
    url(r'^(?P<token>[0-9]+)/game_lobby$', views.wait, name = 'game_lobby')
    #need to add view for game lobby then update line 10 with new view
]
