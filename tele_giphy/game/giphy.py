# Third Party
from requests import get

GIPHY_URL = 'http://api.giphy.com/v1/gifs/'
KEY = 'dc6zaTOxFJmzC'


def _gif_random(tag='american psycho', api_key=KEY, rating=''):
    # See https://github.com/Giphy/GiphyAPI#random-endpoint
    endpoint = GIPHY_URL + 'random'
    params = {'api_key': api_key, 'tag': tag}
    if rating:
        params['rating'] = rating
    data = get(endpoint, params)
    return data


def _gif_translate(string='leeroy', api_key=KEY, rating=''):
    # See https://github.com/Giphy/GiphyAPI#translate-endpoint
    endpoint = GIPHY_URL + 'translate'
    params = {'api_key': api_key, 's': string}
    if rating:
        params['rating'] = rating
    data = get(endpoint, params)
    return data


# Standarize random and translate endpoint returns
def giphy_call(call_type='translate', phrase='doge', api_key=KEY, rating=''):
    data_dict = {'call_type': '',
                 'image_url': '',
                 'phrase': '',
                 'meta': {}}

    if call_type == 'translate':
        api_resp = _gif_translate(string=phrase, api_key=api_key, rating=rating)
        data_dict = standarize_data(data_dict, api_resp, call_type, phrase)
    elif call_type == 'random':
        api_resp = _gif_random(tag=phrase, api_key=api_key, rating=rating)
        data_dict = standarize_data(data_dict, api_resp, call_type, phrase)
    else:
        data_dict['call_type'] = 'error'
    return data_dict


def standarize_data(data_dict, api_resp, call, phrase):
    api_resp_json = api_resp.json()
    data_dict['meta'] = api_resp_json['meta']
    if api_resp.status_code == 200:
        data_dict['call_type'] = call
        data_dict['phrase'] = phrase
        if call == 'translate':
            data_dict['image_url'] = api_resp_json['data']['images']['original']['url']
        if call == 'random':
            data_dict['image_url'] = api_resp_json['data']['image_url']


    return data_dict
