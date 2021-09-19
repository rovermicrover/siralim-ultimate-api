import unittest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TraitsRouterTests(unittest.TestCase):
    def test_index(self):
        response = client.get("/traits/")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 25)

    def test_index_page_size(self):
        response = client.get("/traits/?size=2")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 2)

    def test_index_page(self):
        response1 = client.get("/traits/?page=0&size=2")
        self.assertEqual(response1.status_code, 200)
        json1 = response1.json()
        self.assertEqual(json1["data"][0]["id"], 1)

        response2 = client.get("/traits/?page=1&size=2")
        self.assertEqual(response2.status_code, 200)
        json2 = response2.json()
        self.assertEqual(json2["data"][0]["id"], 3)

    def test_index_sort(self):
        response = client.get("/traits/?sort_by=name&sort_direction=desc")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"][0]["name"], "Zero to One")

    def test_search_filter_name(self):
        response = client.post(
            "/traits/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "material_name",
                            "comparator": "like",
                            "value": "%Figment",
                        },
                        {
                            "field": "tags",
                            "comparator": "&&",
                            "value": ["buff-barrier"],
                        }
                    ]
                },
                "sorting": {"by": "name", "direction": "desc"},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 1)
        self.assertEqual(json["data"][0]["name"], "Call of Time")

    def test_search_filter_id(self):
        response = client.post(
            "/traits/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "id",
                            "comparator": "<=",
                            "value": 4,
                        }
                    ]
                },
                "sorting": {"by": "name", "direction": "desc"},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 4)

    def test_get_id(self):
        response = client.get("/traits/1")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["id"], 1)

    def test_get_slug(self):
        response = client.get("/traits/call-of-time")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["slug"], "call-of-time")
