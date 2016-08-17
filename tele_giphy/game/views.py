from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.

def index(request):
	token = ""
	for i in range(4):
		token = token + random.choice('1234567890')
	return render(request, 'game/index.html', {"token": token})

def wait(request, token):
	return render(request, 'game/wait.html', {"token": token})