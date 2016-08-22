import pytest
import json
from ..giphy import gif_translate, gif_random
import responses
import re
import requests

# Load JSON fixtures
@pytest.fixture(scope='module')
def load_json(request):
    load_file = request.param
    with open(load_file, 'rU') as json_file:
       return(json.load(json_file))

# Tests giphy.gif_random
@pytest.mark.usefixtures('load_json')
@pytest.mark.parametrize("load_json", ['./tests/fixtures/random_001.json'], indirect=True)
class TestRandom:
    @pytest.fixture(autouse=True)
    def setUp(self, load_json):
        self.json = load_json
        responses.add(responses.GET, 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho',
            json=json.dumps(self.json), status=200, match_querystring=True)

    @responses.activate
    def test_random1(self):
        resp = gif_random() # == requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho')
        # resp = requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho')

    @responses.activate
    def test_random2(self):
        resp = gif_random() # == requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho')
        # resp = requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho')

    @responses.activate
    def test_random3(self):
        resp = gif_random() # == requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho')
        # resp = requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho')

# @pytest.mark.usefixtures('load_json')
# @pytest.mark.parametrize("load_json", ['./tests/fixtures/translate_001.json'], indirect=True)
# class TestTranslate():
#     def setUp(self, load_json):
#         self.json = load_json
#         responses.add(responses.GET, 'http://api.giphy.com/v1/gifs/translate?s=leeroy&api_key=dc6zaTOxFJmzC',
#             json=json.dumps(self.json), status=200, content_type='application/json')

#     @responses.activate
#     def test_translate1(self, load_json):
#         # gif_translate()
#         print("Test Random 1")
#         print(load_json['meta'])
#         assert 0
