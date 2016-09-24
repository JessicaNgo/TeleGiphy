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


# Standarize random and translate endpoint returns
def giphy_call(call_type='translate', phrase='doge', api_key=KEY):
    standard_data = {'call_type': '', 'image_url': '', 'phrase': ''}
    if call_type == 'translate':
        resp = _gif_translate(string=phrase, api_key=api_key)
        standard_data['call_type'] = 'translate'
        standard_data['phrase'] = phrase
        standard_data['image_url'] = resp.json()['data']['images']['original']['url']
        return standard_data

    elif call_type == 'random':
        resp = _gif_random(tag=phrase, api_key=api_key)
        standard_data['call_type'] = 'random'
        standard_data['phrase'] = phrase
        standard_data['image_url'] = resp.json()['data']['image_url']
        return standard_data
    else:
        standard_data['call_type'] = 'error'
        return standard_data
