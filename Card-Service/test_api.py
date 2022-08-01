import unittest
import requests

class TestAPI(unittest.TestCase):
    URL = 'http://127.0.0.1:5001/'

    expected_response_200 = {
    "answer": "answer1",
    "id": 1,
    "question": "question1",
    "timestamp": "Mon, 23 May 2022 07:02:26 GMT",
    "topic": "topic1",
    "userId": 2
    }

    expected_response_404 = {
    "message": "No card found!"
    }

    def test_get_one_card_200(self):
        resp = requests.get(self.URL+'card/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 6)
        self.assertDictEqual(resp.json(), self.expected_response_200)
        print('test_get_one_card_200 completed!')

    def test_get_one_card_404(self):
        resp = requests.get(self.URL + 'card/11')
        self.assertEqual(resp.status_code, 404)
        self.assertDictEqual(resp.json(), self.expected_response_404)
        print('test_get_one_card_404 completed!')

if __name__ == "__main__":
    tester = TestAPI()
    tester.test_get_one_card_200()
    tester.test_get_one_card_404()