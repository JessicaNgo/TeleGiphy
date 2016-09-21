# Standard Library
import json
import os

# Third Party
import pytest
import responses

# Localfolder
from ..giphy import (_gif_random as gif_random,
                     _gif_translate as gif_translate,
                     giphy_call)


# Load JSON fixtures
@pytest.fixture(scope='module')
def load_json(request):
    file_name = request.param
    path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', file_name)
    with open(path_to_json, 'rU') as json_file:
        return json.load(json_file)


# Tests where giphy.gif_random get 200
@pytest.mark.parametrize("load_json", ['random_200.json'], indirect=True)
class TestRandomSuccess:
    # Sets up request fixture
    @pytest.fixture(autouse=True)
    def setUp(self, load_json):
        self.json = load_json
        # GET 200 setup
        responses.add(responses.GET,
                      'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=american+psycho',
                      json=json.dumps(self.json), status=200, match_querystring=True)

    @responses.activate
    def testExpectedResponse(self):
        resp = gif_random()
        expected = self.json
        # status is as expected
        assert resp.status_code == 200
        # json is the same between fixture and request
        for item in expected:
            assert item in resp.json()


# Tests where giphy.gif_random get 403
@pytest.mark.parametrize("load_json", ['random_403.json'], indirect=True)
class TestRandomFail:
    # Sets up request fixture
    @pytest.fixture(autouse=True)
    def setUp(self, load_json):
        self.json = load_json
        # GET 403 setup
        # Might want a more comprehensive regex to capture wrong api key
        responses.add(responses.GET,
                      'http://api.giphy.com/v1/gifs/random?api_key=abc&tag=american+psycho',
                      json=self.json, status=403, match_querystring=True)

    @responses.activate
    def testExpectedResponse(self):
        resp = gif_random(api_key='abc')
        expected = self.json
        # status code
        assert resp.status_code == 403
        # json is the same between fixture and request
        for item in expected:
            assert item in resp.json()


# Tests where giphy.gif_translate get 200
@pytest.mark.parametrize("load_json", ['translate_200.json'], indirect=True)
class TestTranslateSuccess:
    # Sets up request fixture
    @pytest.fixture(autouse=True)
    def setUp(self, load_json):
        self.json = load_json
        # GET 403 setup
        # Might want a more comprehensive regex to capture wrong api key
        responses.add(responses.GET,
                      'http://api.giphy.com/v1/gifs/translate?api_key=dc6zaTOxFJmzC&s=leeroy',
                      json=self.json, status=200, match_querystring=True)

    @responses.activate
    def testExpectedResponse(self):
        resp = gif_translate()
        expected = self.json
        # status code
        assert resp.status_code == 200
        # json is the same between fixture and request
        for item in expected:
            assert item in resp.json()


# Tests giphy get 403
@pytest.mark.parametrize("load_json", ['translate_403.json'], indirect=True)
class TestTranslateFail:
    # Sets up request fixture
    @pytest.fixture(autouse=True)
    def setUp(self, load_json):
        self.json = load_json
        # GET 403 setup
        # Might want a more comprehensive regex to capture wrong api key
        responses.add(responses.GET,
                      'http://api.giphy.com/v1/gifs/translate?api_key=abc&s=leeroy',
                      json=self.json, status=403, match_querystring=True)

    @responses.activate
    def testExpectedResponse(self):
        resp = gif_translate(api_key='abc')
        expected = self.json
        # status code
        assert resp.status_code == 403
        # json is the same between fixture and request
        for item in expected:
            assert item in resp.json()

# Temp function for funnel
def loadin_json(filename):
    path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', filename)
    with open(path_to_json, 'rU') as json_file:
        return json.load(json_file)


# Test giphy funnel success
@pytest.mark.parametrize("json_file", ['translate_200.json', 'random_200.json'])
@pytest.mark.parametrize("status", [200])
class TestGiphyFunnelSuccess:
    # Sets up request fixture;
    @pytest.fixture(autouse=True)
    def setUp(self, json_file, status):
        self.json = loadin_json(json_file)
        # GET translate setup
        responses.add(responses.GET,
                      'http://api.giphy.com/v1/gifs/translate?api_key=dc6zaTOxFJmzC&s=doge',
                      json=self.json, status=status, match_querystring=True)        
        responses.add(responses.GET,
                      'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=doge',
                      json=self.json, status=status, match_querystring=True)

    @responses.activate
    def testExpectedResponseTraslate(self):
        resp = giphy_call()
        expected = self.json
        assert resp.status_code == 200
        # Check json
        loaded_json = resp.json()
        # json is the same between fixture and request
        assert expected == loaded_json 
