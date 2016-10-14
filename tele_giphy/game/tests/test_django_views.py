from django.test import Client, TestCase, RequestFactory
import unittest

c = Client()

class TestIndexResponses(TestCase):
    def test_get_index_return_200(self):
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_index_return_405(self):
        response = c.post('/')
        self.assertEqual(response.status_code, 405)

    def test_put_index_return_405(self):
        response = c.put('/')
        self.assertEqual(response.status_code, 405)


class TestNewGameResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_new_game_return_200(self):
        response = c.get('/new_game', {'game_mode': 'hotseat'})
        self.assertEqual(response.status_code, 200)

    def test_post_new_game_return_302_game_lobby(self):
        response = c.post('/new_game', {'game_mode': 'hotseat'})
        self.assertEqual(response.status_code, 302)

    def test_put_new_game_return_405(self):
        response = c.put('/new_game')
        self.assertEqual(response.status_code, 405)

    def test_poast_new_game_return_302_index(self):
        # Create an integrity error
        pass

class TestJoinGameResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post_join_game_return_302(self):
        response = c.post('/join_game',{'join_token': '1234'})
        self.assertEqual(response.status_code, 302)

    def test_get_put_join_game_return_405(self):
        response = c.get('/join_game')
        self.assertEqual(response.status_code, 405)
        response = c.put('/join_game')
        self.assertEqual(response.status_code, 405)


class TestPreGameRoomResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_pre_game_room_no_token_return_404(self):
        response = c.get('/pre_game_room/')
        self.assertEqual(response.status_code, 404)

    def test_get_pre_game_room_with_token_return_404(self):
        response = c.get('/pre_game_room/1010/')
        self.assertEqual(response.status_code, 200)

    def test_post_put_pre_game_room_with_token_return_304(self):
        response = c.post('/pre_game_room/1010/')
        self.assertEqual(response.status_code, 304)
        response = c.put('/pre_game_room/1010/')
        self.assertEqual(response.status_code, 304)


class TestStartGameResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class TestChooseNameResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class TestGameplayContextResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class TestMultiGameplayContextResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class TestHotSeatGameplayResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class TestChooseNewGifResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class TestPassOnResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class TestMultiGameplayResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class TestWaitingRoomResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class TestGameoverResponses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()