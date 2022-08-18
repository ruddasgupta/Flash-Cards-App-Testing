import json
import random

try:
    from app import app
    import unittest
except Exception as e:
    print("Some Modules are Missing {} ".format(e))

class TestScore(unittest.TestCase):

    def test_create_score_201(self):
        tester = app.test_client(self)
        response = tester.post("/score", json={
            'cardId': str(random.randint(1000, 10000)),
            'userId': str(random.randint(1000, 10000))
        })
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 201)
        self.assertEqual(content_type, "application/json")

    def test_get_total_score_200(self):
        tester = app.test_client(self)
        response = tester.get("/totalscore/1")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 200)
        self.assertEqual(content_type, "application/json")

    def test_get_score_of_card_200(self):
        tester = app.test_client(self)
        response = tester.get("/score/card/1")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 200)
        self.assertEqual(content_type, "application/json")

    def test_get_score_of_card_404(self):
        tester = app.test_client(self)
        response = tester.get("/score/card/11")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 404)
        self.assertEqual(content_type, "application/json")

    def test_increment_score_200(self):
        tester = app.test_client(self)
        response = tester.put("/score/increment/2")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 202)
        self.assertEqual(content_type, "application/json")

    def test_increment_attempts_200(self):
        tester = app.test_client(self)
        response = tester.put("/attempts/increment/2")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 202)
        self.assertEqual(content_type, "application/json")

    def test_increment_score_404(self):
        tester = app.test_client(self)
        response = tester.put("/score/increment/22")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 404)
        self.assertEqual(content_type, "application/json")

    def test_increment_attempts_404(self):
        tester = app.test_client(self)
        response = tester.put("/attempts/increment/22")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 404)
        self.assertEqual(content_type, "application/json")

    def test_delete_score_200(self):
        tester = app.test_client(self)
        score = tester.post("/score", json={
            'cardId': str(random.randint(1000, 10000)),
            'userId': str(random.randint(1000, 10000))
        })
        response = tester.delete("/score/card/" + str(score.get_json()['cardId']))
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 200)
        self.assertEqual(content_type, "application/json")

    def test_delete_score_404(self):
        tester = app.test_client(self)
        response = tester.delete("/score/card/222")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 404)
        self.assertEqual(content_type, "application/json")

    def test_delete_all_score_200(self):
        tester = app.test_client(self)
        score = tester.post("/score", json={
            'cardId': str(random.randint(1000, 10000)),
            'userId': str(random.randint(1000, 10000))
        })
        response = tester.delete("/score/user/" + str(score.get_json()['userId']))
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 200)
        self.assertEqual(content_type, "application/json")
 
    @unittest.skip("Skip Test")
    def test_delete_all_score_404_Skip(self):
        tester = app.test_client(self)
        response = tester.delete("/score/user/222")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 404)
        self.assertEqual(content_type, "application/json")

    @unittest.expectedFailure
    def test_delete_all_score_404_Failure(self):
        tester = app.test_client(self)
        response = tester.delete("/score/user/222")
        status_code = response.status_code
        content_type = response.content_type
        self.assertEqual(status_code, 200)
        self.assertEqual(content_type, "application/json")

if __name__ == "__main__":
    unittest.main()
