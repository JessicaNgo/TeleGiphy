from requests import get

giphy_url = 'http://api.giphy.com/v1/gifs/'
key = 'dc6zaTOxFJmzC'

def gif_random(tag='doge', api_key=key):
    # http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho
    endpoint = giphy_url + 'random'
    params = {'api_key':api_key,'tag':tag}
    response = get(endpoint, params)
    response_json = response.json()
    return response_json

def gif_translate(string='doge', api_key=key):
    # http://api.giphy.com/v1/gifs/translate?s=superman&api_key=dc6zaTOxFJmzC
    endpoint = giphy_url + 'translate'
    params = {'api_key':api_key,'s':string}
    response = get(endpoint, params)
    response_json = response.json()
    return response_json