import unittest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class PerksRouterTests(unittest.TestCase):
    def test_index(self):
        response = client.get("/perks/")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 25)

    def test_index_page_size(self):
        response = client.get("/perks/?size=2")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 2)

    def test_index_page(self):
        response1 = client.get("/perks/?page=0&size=2")
        self.assertEqual(response1.status_code, 200)
        json1 = response1.json()
        self.assertEqual(json1["data"][0]["id"], 1)

        response2 = client.get("/perks/?page=1&size=2")
        self.assertEqual(response2.status_code, 200)
        json2 = response2.json()
        self.assertEqual(json2["data"][0]["id"], 3)

    def test_index_sort(self):
        response = client.get("/perks/?sort_by=name&sort_direction=desc")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"][0]["name"], "Zoom")

    def test_search_filter_name(self):
        response = client.post(
            "/perks/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "name",
                            "comparator": "like",
                            "value": "%Blazing%",
                        },
                    ]
                },
                "sorting": {"by": "name", "direction": "asc"},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 1)
        self.assertEqual(json["data"][0]["name"], "Blazing Soul")

    def test_search_filter_id(self):
        response = client.post(
            "/perks/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "id",
                            "comparator": ">=",
                            "value": 4,
                        },
                        {
                            "field": "id",
                            "comparator": "<=",
                            "value": 8,
                        },
                    ]
                },
                "sorting": {"by": "name", "direction": "desc"},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 5)

    def test_search_filter_ascension(self):
        response = client.post(
            "/perks/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "ascension",
                            "comparator": "==",
                            "value": True,
                        },
                    ]
                },
                "sorting": {"by": "name", "direction": "asc"},
                "pagination": {"size": 50},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 30)
        self.assertEqual(json["data"][0]["name"], "Amalgamation")

    def test_get_id(self):
        response = client.get("/perks/1")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["id"], 1)

    def test_get_slug(self):
        response = client.get("/perks/blazing-soul")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["slug"], "blazing-soul")

    def test_get_not_found(self):
        response = client.get("/perks/foobar")
        self.assertEqual(response.status_code, 404)
