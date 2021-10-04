import unittest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class SpecializationsRouterTests(unittest.TestCase):
    def test_index(self):
        response = client.get("/specializations/")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 30)

    def test_index_page_size(self):
        response = client.get("/specializations/?size=2")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 2)

    def test_index_page(self):
        response1 = client.get("/specializations/?page=0&size=2")
        self.assertEqual(response1.status_code, 200)
        json1 = response1.json()
        self.assertEqual(json1["data"][0]["id"], 1)

        response2 = client.get("/specializations/?page=1&size=2")
        self.assertEqual(response2.status_code, 200)
        json2 = response2.json()
        self.assertEqual(json2["data"][0]["id"], 3)

    def test_index_sort(self):
        response = client.get(
            "/specializations/?sort_by=name&sort_direction=desc"
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"][0]["name"], "Witch Doctor")

    def test_search_filter_name(self):
        response = client.post(
            "/specializations/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "name",
                            "comparator": "ilike",
                            "value": "Evok%",
                        }
                    ]
                },
                "sorting": {"by": "name", "direction": "desc"},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 1)
        self.assertEqual(json["data"][0]["name"], "Evoker")

    def test_search_filter_id(self):
        response = client.post(
            "/specializations/search",
            json={
                "filter": {
                    "filters": [
                        {
                            "field": "id",
                            "comparator": ">",
                            "value": 1,
                        }
                    ]
                },
                "sorting": {"by": "name", "direction": "desc"},
            },
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 29)

    def test_get_id(self):
        response = client.get("/specializations/1")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["id"], 1)

    def test_get_slug(self):
        response = client.get("/specializations/evoker")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["slug"], "evoker")

    def test_get_not_found(self):
        response = client.get("/specializations/foobar")
        self.assertEqual(response.status_code, 404)
