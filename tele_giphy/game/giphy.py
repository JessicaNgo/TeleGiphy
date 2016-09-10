# Third Party
from requests import get

GIPHY_URL = 'http://api.giphy.com/v1/gifs/'
KEY = 'dc6zaTOxFJmzC'


def _gif_random(tag='american psycho', api_key=KEY):
    # See https://github.com/Giphy/GiphyAPI#random-endpoint
    endpoint = GIPHY_URL + 'random'
    params = {'api_key': api_key, 'tag': tag}
    data = get(endpoint, params)
    return data


def _gif_translate(string='leeroy', api_key=KEY):
    # See https://github.com/Giphy/GiphyAPI#translate-endpoint
    endpoint = GIPHY_URL + 'translate'
    params = {'api_key': api_key, 's': string}
    data = get(endpoint, params)
    return data

def giphy_call(call_type='translate', string='doge'):
    if call_type == 'translate':
        pass
    elif call_type == 'random':
        pass
    else:
        pass
