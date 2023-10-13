from django.test import TestCase

import json
from mapbackend.tests import BaseTestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from points.models import UserPoint


class UserPointTests(BaseTestCase):
    fixtures = ["../fixtures/test_data.json"]

    def test_get_userpoints(self):
        """Check that getting userpoints works"""
        client = APIClient()
        response = client.get("/userpoints/")
        self.assertEqual(response.status_code, 200)

    def test_get_single_userpoint(self):
        """Check that getting a single userpoint works"""
        client = APIClient()
        response = client.get("/userpoints/333/")
        response_data = response.json()

        expected_data = {
            "pk": 333,
            "label_text": "Helsinki central railway station",
            "user_id": 222,
            "position": {'coordinates': [24.94030214683831, 60.1712000939996], 'type': 'Point'},
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, expected_data)

    def test_user_post_userpoint(self):
        """User should be able to create a new userpoint"""
        user = get_user_model().objects.get(pk=333)
        # fetch JWT token
        token = self.get_access_token(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

        data = {
            "label_text": "Point label text",
            "position": {
                "coordinates": [24.95077731787692, 60.17048552960218], "type": "Point"
            }
        }

        response = client.post("/userpoints/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        expected_data = {
            "pk": UserPoint.objects.last().pk,
            "user_id": user.pk,
            **data
        }

        self.assertEqual(response.json(), expected_data)


    def test_user_update_userpoint(self):
        """User should be allowed to update their own userpoints"""
        user = get_user_model().objects.get(pk=333)
        # fetch JWT token
        token = self.get_access_token(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

        data = {
            "label_text": "Changed label"
        }

        expected_data = {
            "pk": 444,
            "user_id": 333,
            "label_text": "Changed label",
            "position": {
                "coordinates": [24.95077731787692, 60.17048552960218], "type": "Point"
            }
        }

        response = client.put(
            "/userpoints/444/",
            json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        response = client.get("/userpoints/444/")
        self.assertEqual(response.json(), expected_data)


