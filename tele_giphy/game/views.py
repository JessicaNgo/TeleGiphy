from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import random

# Create your views here.

def index(request):
	return render(request, 'game/index.html')

def new_game(request):
	token = str(random.randint(1000,9999))
	return HttpResponseRedirect(reverse('game:waiting_lobby', args = (token,)))

def wait(request, token):
	return render(request, 'game/wait.html', {"token": token})

def gameover(request):
    return render(request, 'game/gameover.html')

	
# / index
# new game => /new_game => generate token and redirect to waiting lobby
# /waiting_lobby/<token>