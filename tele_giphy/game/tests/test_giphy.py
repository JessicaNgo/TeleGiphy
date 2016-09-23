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


BASE_GIPHY_URL = "http://api.giphy.com/v1/gifs/"


# Load json file
def load_json(filename):
    path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', filename)
    with open(path_to_json, 'rU') as json_file:
        return json.load(json_file)


@pytest.mark.parametrize("json_filename", ['translate_200.json', 'random_200.json'])
class TestTranslateSuccess:
    # Sets up request fixture
    @pytest.fixture(autouse=True)
    def setUp(self, json_filename):
        self.status = 200
        self.json = load_json(json_filename)
        if 'translate' in json_filename:
            url = BASE_GIPHY_URL + "translate?api_key=dc6zaTOxFJmzC&s=doge"
        elif 'random' in json_filename:
            url = BASE_GIPHY_URL + "random?api_key=dc6zaTOxFJmzC&tag=doge"
        else:
            raise ValueError
        responses.add(responses.GET, url, json=self.json,
                      status=self.status, match_querystring=True)

    @responses.activate
    def testExpectedResponse(self, json_filename):
        if 'translate' in json_filename:
            resp = gif_translate(string='doge', api_key='dc6zaTOxFJmzC')
            expected = load_json("translate_{}.json".format(self.status))
        elif 'random' in json_filename:
            resp = gif_random(tag='doge', api_key='dc6zaTOxFJmzC')
            expected = load_json("random_{}.json".format(self.status))
        else:
            raise ValueError
        expected = self.json
        # status code
        assert resp.status_code == 200
        # json is the same between fixture and request
        for item in expected:
            assert item in resp.json()


# Tests non-funnel giphy get 403
@pytest.mark.parametrize("json_filename", ['translate_403.json', 'random_403.json'])
class TestTranslateFail:
    # Sets up request fixture
    @pytest.fixture(autouse=True)
    def setUp(self, json_filename):
        self.status = 403
        self.json = load_json(json_filename)
        if 'translate' in json_filename:
            url = BASE_GIPHY_URL + "translate?api_key=abc&s=doge"
        elif 'random' in json_filename:
            url = BASE_GIPHY_URL + "random?api_key=abc&tag=doge"
        else:
            raise ValueError
        responses.add(responses.GET, url, json=self.json,
                      status=self.status, match_querystring=True)

    @responses.activate
    def testExpectedResponse(self, json_filename):
        if 'translate' in json_filename:
            resp = gif_translate(api_key='abc', string='doge')
            expected = load_json("translate_{}.json".format(self.status))
        elif 'random' in json_filename:
            resp = gif_random(api_key='abc', tag='doge')
            expected = load_json("random_{}.json".format(self.status))
        else:
            raise ValueError
        expected = self.json
        # status code
        assert resp.status_code == 403
        # json is the same between fixture and request
        for item in expected:
            assert item in resp.json()


# Test giphy funnel success
@pytest.mark.parametrize("json_filename", ['translate_200.json', 'random_200.json'])
class TestGiphyFunnelSuccess:
    # Sets up request fixture;
    @pytest.fixture(autouse=True)
    def setUp(self, json_filename):
        self.status = 200
        self.json = load_json(json_filename)
        if 'translate' in json_filename:
            url = BASE_GIPHY_URL + "translate?api_key=dc6zaTOxFJmzC&s=doge"
        elif 'random' in json_filename:
            url = BASE_GIPHY_URL + "random?api_key=dc6zaTOxFJmzC&tag=doge"
        else:
            raise ValueError
        responses.add(responses.GET, url, json=self.json,
                      status=self.status, match_querystring=True)

    @responses.activate
    def testExpectedResponse(self, json_filename):
        if 'random' in json_filename:
            resp = giphy_call(call_type='random')
            expected = load_json("random_{}.json".format(self.status))
        else:
            resp = giphy_call()
            expected = load_json("random_{}.json".format(self.status))
        expected = self.json
        assert resp.status_code == 200
        # Check json
        loaded_json = resp.json()
        assert expected == loaded_json
        assert loaded_json['meta']['status'] == 200


# Test giphy funnel fail
@pytest.mark.parametrize("json_filename", ['translate_403.json', 'random_403.json'])
class TestGiphyFunnelFail:
    # Sets up request fixture;
    @pytest.fixture(autouse=True)
    def setUp(self, json_filename):
        self.status = 403
        self.json = load_json(json_filename)
        if 'translate' in json_filename:
            url = BASE_GIPHY_URL + "translate?api_key=abc&s=doge"
        elif 'random' in json_filename:
            url = BASE_GIPHY_URL + "random?api_key=abc&tag=doge"
        else:
            raise ValueError
        responses.add(responses.GET, url, json=self.json,
                      status=self.status, match_querystring=True)

    @responses.activate
    def testExpectedResponse(self, json_filename):
        if 'random' in json_filename:
            resp = giphy_call(call_type='random', api_key='abc')
            expected = load_json("random_{}.json".format(self.status))
        else:
            resp = giphy_call(api_key='abc')
            expected = load_json("translate_{}.json".format(self.status))
        assert resp.status_code == 403
        # Check json
        loaded_json = resp.json()
        assert expected == loaded_json
        assert loaded_json['meta']['status'] == 403
