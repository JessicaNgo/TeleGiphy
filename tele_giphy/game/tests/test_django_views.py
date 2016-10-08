from django.test import Client
import unittest


class TestIndex(unittest.TestCase):
    def test_get_index_return_200(self):
        c = Client()
        response = c.get('/')
        # print(response.content)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.content, 200)

    def test_post_index_return_405(self):
        c = Client()
        response = c.post('/')
        print(response)
        self.assertEqual(response.status_code, 405)
