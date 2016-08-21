import pytest
import json
from ..giphy import gif_translate, gif_random
import responses
import requests

# Load JSON fixtures
@pytest.fixture(scope='module')
def load_json(request):
    load_file = request.param
    with open(load_file, 'rU') as json_file:
       return(json.load(json_file))

# def setUp(self, load_json):
#     self.json = load_json
#     responses.add(responses.GET, 'http://api.giphy.com/v1/gifs/random', 
#         json=json.dumps(self.json), status=200, content_type='application/json')



@pytest.mark.usefixtures('load_json')
@pytest.mark.parametrize("load_json", ['./tests/fixtures/random_001.json'], indirect=True)
class TestRandom():
    @responses.activate
    def test_random1(self, load_json):
        # gif_random()
        print("Test Random 1")
        print(load_json['meta'])
        assert 0

# @responses.activate
@pytest.mark.usefixtures('load_json')
@pytest.mark.parametrize("load_json", ['./tests/fixtures/translate_001.json'], indirect=True)
class TestTranslate():
    def test_translate1(self, load_json):
        # gif_translate()
        print("Test Random 1")
        print(load_json['meta'])
        assert 0
