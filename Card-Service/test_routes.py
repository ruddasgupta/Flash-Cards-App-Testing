import json
from jsonschema import validate
from jsonschema import Draft6Validator
import requests

class TestRoutes:
    URL = 'http://127.0.0.1:5001/'

    schema_200 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "properties": {
            "answer": {
            "type": "string"
            },
            "id": {
            "type": "integer"
            },
            "question": {
            "type": "string"
            },
            "timestamp": {
            "type": "string"
            },
            "topic": {
            "type": "string"
            },
            "userId": {
            "type": "integer"
            }
        },
        "required": [
            "answer",
            "id",
            "question",
            "timestamp",
            "topic",
            "userId"
        ]
    }

    schema_404 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "properties": {
            "message": {
            "type": "string"
            }
        },
        "required": [
            "message"
        ]
    }

    schema_get_all_cards_200 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "properties": {
            "cards": {
            "type": "array",
            "items": [
                {
                "type": "object",
                "properties": {
                    "answer": {
                    "type": "string"
                    },
                    "id": {
                    "type": "integer"
                    },
                    "question": {
                    "type": "string"
                    },
                    "timestamp": {
                    "type": "string"
                    },
                    "topic": {
                    "type": "string"
                    },
                    "userId": {
                    "type": "integer"
                    }
                },
                "required": [
                    "answer",
                    "id",
                    "question",
                    "timestamp",
                    "topic",
                    "userId"
                ]
                }
            ]
            }
        },
        "required": [
            "cards"
        ]
    }

    schema_get_all_cards_404 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "properties": {
            "cards": {
            "type": "array",
            "items": {}
            }
        },
        "required": [
            "cards"
        ]
    }

    def test_get_one_card_200(self):
        resp = requests.get(self.URL+'card/1')
        assert resp.status_code == 200
        assert len(resp.json()) == 6
        validate(instance=resp, schema=self.schema_200)
        print('test_get_one_card_200 completed!')

    def test_get_one_card_404(self):
        resp = requests.get(self.URL + 'card/11')
        assert resp.status_code == 404
        validate(instance=resp, schema=self.schema_404)
        print('test_get_one_card_404 completed!')

    def test_get_all_cards_200(self):
        resp = requests.get(self.URL+'card/user/1')
        assert resp.status_code == 200
        validate(instance=resp, schema=self.schema_get_all_cards_200)
        print('test_get_one_card_200 completed!')

    def test_get_all_cards_404(self):
        resp = requests.get(self.URL + 'card/user/11')
        assert resp.status_code == 200
        validate(instance=resp, schema=self.schema_get_all_cards_404)
        print('test_get_one_card_404 completed!')