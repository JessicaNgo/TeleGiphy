from django.http import HttpRequest
from requests import get

giphy_url = 'http://api.giphy.com/v1/gifs/'
key = 'dc6zaTOxFJmzC'

def random(tag='american+psycho', api_key=key):
    # http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho
    endpoint = giphy_url + 'random'
    params = {'api_key':api_key,'tag':tag}
    data = get(endpoint, params)
    return data

# def translate(tag='american+psycho', api_key=key):
#     # http://api.giphy.com/v1/gifs/translate?s=superman&api_key=dc6zaTOxFJmzC
#     endpoint = giphy_url + 'translate'
#     params = {'api_key':api_key,'tag':tag}
#     data = get(endpoint, params)
#     return data