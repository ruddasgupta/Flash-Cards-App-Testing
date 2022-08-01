import unittest
import requests

class TestAPI(unittest.TestCase):
    URL = 'http://127.0.0.1:5002/'

    expected_response_200 = {
    "attempts": 0,
    "cardId": 1,
    "id": 1,
    "score": 0,
    "timestamp": "Mon, 23 May 2022 07:02:26 GMT",
    "userId": 2
    }

    expected_response_404 = {
    "message": "No card found!"
    }

    def test_get_total_score_200(self):
        resp = requests.get(self.URL + 'score/card/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 6)
        self.assertDictEqual(resp.json(), self.expected_response_200)
        print('test_get_total_score_200 completed!')

    def test_get_total_score_404(self):
        resp = requests.get(self.URL + 'score/card/11')
        self.assertEqual(resp.status_code, 404)
        self.assertDictEqual(resp.json(), self.expected_response_404)
        print('test_get_total_score_404 completed!')

if __name__ == "__main__":
    tester = TestAPI()
    tester.test_get_total_score_200()
    tester.test_get_total_score_404()