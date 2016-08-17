from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<token>[0-9]+)/$', views.wait, name='wait'),
]