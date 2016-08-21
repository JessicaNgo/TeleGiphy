import pytest
import json
from ..giphy import gif_translate, gif_random

# Load fixtures
@pytest.fixture(scope='module')
def load_json(request):
    load_file = request.param
    with open(load_file, 'rU') as json_file:
       return(json.load(json_file))

@pytest.mark.usefixtures('load_json')
@pytest.mark.parametrize("load_json", ['./tests/fixtures/random_001.json'], indirect=True)
class TestRandom():
    def test_random1(self, load_json):
        print("Test Random 1")
        print(load_json['meta'])
        assert 0
    def test_random2(self):
        print("Test Random 2")
        assert 0

