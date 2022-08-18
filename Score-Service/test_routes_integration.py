from test_base import BaseTestCase

class ScoreIntegrationTests(BaseTestCase):
    
    def test_get_total_score_200(self):
        response = self.client.get('score/card/1')
        self.assert200(response)
        self.assertEqual(response.json, {
            "attempts": 12,
            "cardId": 1,
            "id": 1,
            "score": 6,
            "timestamp": "Mon, 23 May 2022 07:02:26 GMT",
            "userId": 2
        })