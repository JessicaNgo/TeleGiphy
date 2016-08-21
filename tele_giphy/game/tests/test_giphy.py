import pytest
import json
from ..giphy import gif_translate, gif_random
import responses

# Load JSON fixtures
@pytest.fixture(scope='module')
def load_json(request):
    load_file = request.param
    with open(load_file, 'rU') as json_file:
       return(json.load(json_file))

@responses.activate
@pytest.mark.usefixtures('load_json')
@pytest.mark.parametrize("load_json", ['./tests/fixtures/random_001.json'], indirect=True)
class TestRandom():
    def test_random1(self, load_json):
        gif_random()
        print("Test Random 1")
        print(load_json['meta'])
        assert 0

@responses.activate
@pytest.mark.usefixtures('load_json')
@pytest.mark.parametrize("load_json", ['./tests/fixtures/translate_001.json'], indirect=True)
class TestTranslate():
    def test_random1(self, load_json):
        gif_translate()
        print("Test Random 1")
        print(load_json['meta'])
        assert 0
