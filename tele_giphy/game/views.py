from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.

def index(request):
	token = ""
	token = str(random.randint(1000,9999))
	return render(request, 'game/index.html', {"token": token})

def wait(request, token):
	return render(request, 'game/wait.html', {"token": token})
