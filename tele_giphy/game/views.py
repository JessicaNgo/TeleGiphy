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
    # Needs to fetchall records for a particular game
    # For each player, get all associated rounds in order
    
    # mock result for html formatting
    result = [
        {'player': 'player1', 'rounds': 
            [{'user_text': 'american psycho', 'giphy_url': 'http://media4.giphy.com/media/6nJ4uNiOwGqty/giphy.gif'},
            {'user_text': 'christian bale', 'giphy_url': 'https://media3.giphy.com/media/yaYw1xR88ccJa/giphy.gif'}, 
            {'user_text': 'kissing', 'giphy_url': 'http://media1.giphy.com/media/3o72F3zlbWvP4kJp4c/giphy.gif'}]},
        {'player': 'professor oak', 'rounds': 
            [{'user_text': 'starter pokemon', 'giphy_url': 'http://media1.giphy.com/media/v6DHXicvXwJHi/giphy.gif'}
            {'user_text': 'fire fox pokemon', 'giphy_url': 'http://media1.giphy.com/media/L2jkcvfvxkpby/giphy.gif'}
            {'user_text': 'team ash pkmn', 'giphy_url': 'http://media4.giphy.com/media/eox3BwD5LHAQw/giphy.gif'}]},
        {'player': 'shibe', 'rounds':
            [{'user_text': 'doge', 'giphy_url': 'https://media4.giphy.com/media/2FnQsl7O3aBC9O/giphy.gif'},
            {'user_text': 'store shibe', 'giphy_url': 'http://media0.giphy.com/media/V2zGGB4ZWE5DW/giphy.gif'},
            {'user_text': 'weird store', 'giphy_url': 'http://media4.giphy.com/media/a0FuEjOWAxIuk/giphy.gif'}]}
    ]

    return render(request, 'game/gameover.html', {"result":result})


'''
round_number = models.IntegerField()
user_text = models.CharField(max_length=150)
giphy_url = models.CharField(max_length=2083)
user = models.ForeignKey(User, on_delete=models.CASCADE)
game = models.ForeignKey(Game, on_delete=models.CASCADE)
'''
	
# / index
# new game => /new_game => generate token and redirect to waiting lobby
# /waiting_lobby/<token>