import unittest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

class ClassesRouterTests(unittest.TestCase):

    def test_index(self):
        response = client.get("/classes/")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 5)

    def test_index_page_size(self):
        response = client.get("/classes/?size=2")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json["data"]), 2)

    def test_index_page(self):
        response1 = client.get("/classes/?page=0&size=2")
        self.assertEqual(response1.status_code, 200)
        json1 = response1.json()
        self.assertEqual(json1["data"][0]["id"], 1)

        response2 = client.get("/classes/?page=1&size=2")
        self.assertEqual(response2.status_code, 200)
        json2 = response2.json()
        self.assertEqual(json2["data"][0]["id"], 3)

    def test_index_sort(self):
        response = client.get("/classes/?sort_by=name&sort_direction=desc")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"][0]["name"], "Sorcery")

    def test_get_id(self):
        response = client.get("/classes/1")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["id"], 1)

    def test_get_slug(self):
        response = client.get("/classes/death")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["data"]["slug"], "death")