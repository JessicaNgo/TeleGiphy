import pytest
import json
from ..giphy import gif_translate, gif_random

# Load fixtures
@pytest.fixture(scope='module')
def load_random_json(load_file='./tests/fixtures/random_001.json'):
    with open(load_file, 'rU') as json_file:
       return(json.load(json_file))

@pytest.mark.usefixtures('load_random_json')
class TestRandom():
    def test_random1(self, load_random_json):
        print("Test Random 1")
        print(load_random_json['meta'])
        assert 0
    def test_random2(self):
        print("Test Random 2")
        assert 0

