import unittest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class CreaturesRouterTests(unittest.TestCase):
    def test_index(self):
        response = client.get("/creatures/")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 25)

    def test_index_page_size(self):
        response = client.get("/creatures/?size=2")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 2)

    def test_index_page(self):
        response1 = client.get("/creatures/?page=0&size=2")
        self.assertEqual(response1.status_code, 200)
        json1 = response1.json()
        self.assertEqual(json1["data"][0]["id"], 1)

        response2 = client.get("/creatures/?page=1&size=2")
        self.assertEqual(response2.status_code, 200)
        json2 = response2.json()
        self.assertEqual(json2["data"][0]["id"], 3)

    def test_index_sort(self):
        response = client.get("/creatures/?sort_by=name&sort_direction=desc")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"][0]["name"], "Zzyia Apocalypse")

    def test_search_filter_name(self):
        response = client.post(
            "/creatures/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "name",
                            "comparator": "ilike",
                            "value": "Zont%",
                        }
                    ]
                },
                "sorting": {"by": "name", "direction": "desc"},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 1)
        self.assertEqual(json["data"][0]["name"], "Zonte")

    def test_search_filter_id(self):
        response = client.post(
            "/creatures/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "id",
                            "comparator": ">",
                            "value": 1,
                        },
                        {
                            "field": "id",
                            "comparator": "<",
                            "value": 6,
                        },
                    ]
                },
                "sorting": {"by": "name", "direction": "desc"},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 4)

    def test_search_filter_trait_tags(self):
        response = client.post(
            "/creatures/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "trait_tags",
                            "comparator": "&&",
                            "value": ["buff-savage"],
                        }
                    ]
                },
                "sorting": {"by": "name", "direction": "desc"},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 5)

    def test_search_filter_id(self):
        response = client.post(
            "/creatures/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "id",
                            "comparator": ">",
                            "value": None,
                        },
                    ]
                },
                "sorting": {"by": "name", "direction": "desc"},
            },
        )
        self.assertEqual(response.status_code, 422)

    def test_get_id(self):
        response = client.get("/creatures/1")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["id"], 1)

    def test_get_slug(self):
        response = client.get("/creatures/zonte")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["slug"], "zonte")

    def test_get_not_found(self):
        response = client.get("/creatures/foobar")
        self.assertEqual(response.status_code, 404)
