from django.test import TestCase
from django.urls import reverse

import json
from mapbackend.tests import BaseTestCase
from django.contrib.auth import get_user_model
from points.models import UserPoint


class UserPointTests(BaseTestCase):
    """Tests concerning the API `/userpoints/` endpoint."""

    list_view_name = "api:userpoint-list"
    detail_view_name = "api:userpoint-detail"
    # reverse the url in case they're changed in the url config

    def setUp(self):
        super(UserPointTests, self).setUp()

    def test_get_userpoints(self):
        """Check that getting userpoints works"""
        client = self.get_client(self.user)
        response = client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_get_single_userpoint(self):
        """Check that getting a single userpoint works"""
        client = self.get_client(self.user)
        response = client.get(self.detail_url(333))
        response_data = response.json()

        expected_data = {
            "id": 333,
            "label_text": "Helsinki central railway station",
            "position": {
                "coordinates": [24.94030214683831, 60.1712000939996],
                "type": "Point",
            },
            "user": {"id": 222, "username": "administrator"},
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, expected_data)

    def test_user_create_userpoint(self):
        """User should be able to create a new userpoint."""

        client = self.get_client(self.user)

        data = {
            "label_text": "Point label text",
            "position": {
                "coordinates": [24.95077731787692, 60.17048552960218],
                "type": "Point",
            },
        }

        response = client.post(
            self.list_url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        expected_data = {
            "id": UserPoint.objects.last().id,
            "user": {"id": 333, "username": "Martin Mapper"},
            **data,
        }

        self.assertEqual(response.json(), expected_data)

    def test_user_update_userpoint(self):
        """User should be allowed to update their own userpoints"""
        # fetch JWT token
        client = self.get_client(self.user)

        data = {"label_text": "Changed label"}

        expected_data = {
            "id": 444,
            "user": {"id": 333, "username": "Martin Mapper"},
            "label_text": "Changed label",
            "position": {
                "coordinates": [24.95077731787692, 60.17048552960218],
                "type": "Point",
            },
        }

        response = client.put(
            self.detail_url(444), json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        response = client.get(self.detail_url(444))
        self.assertEqual(response.json(), expected_data)

    def test_user_delete_userpoint(self):
        """User should be allowed to delete their own userpoints."""
        client = self.get_client(self.user)

        # create new point for test
        point_to_delete = UserPoint.objects.create(label_text="Foo", user=self.user)
        point_id = point_to_delete.id
        response = client.delete(self.detail_url(point_id))

        # server should tell us that the delete was successful
        self.assertEqual(response.status_code, 204)

        # the userpoint should have been deleted from the db
        deleted_point = UserPoint.objects.filter(pk=point_id).first()
        self.assertIsNone(deleted_point)

    def test_user_not_allow_update(self):
        """Users shouldn't be allowed to update userpoints that don't belong to them."""
        client = self.get_client(self.user)

        point = UserPoint.objects.create(label_text="Foo", user=self.admin_user)

        data = {"label_text": "Changed label"}

        response = client.put(
            self.detail_url(point.id), json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)

        # the data should be unchanged
        self.assertEquals(point.label_text, "Foo")

    def test_user_not_allow_delete(self):
        """Users shouldn't be allowed to delete userpoints that don't belong to them."""
        client = self.get_client(self.user)

        point = UserPoint.objects.create(label_text="Foo", user=self.admin_user)

        response = client.delete(
            self.detail_url(point.id),
        )

        self.assertEqual(response.status_code, 403)
        # the point should still be there
        self.assertIsNotNone(UserPoint.objects.filter(pk=point.id).first())

    def test_admin_allow_update(self):
        """Admins should be allowed to update any userpoints they want."""
        client = self.get_client(self.admin_user)

        points = [
            UserPoint.objects.create(label_text="Foo", user=self.user),
            UserPoint.objects.create(label_text="Foo", user=self.admin_user),
            UserPoint.objects.create(label_text="Foo", user=None),
        ]

        data = {"label_text": "Changed label"}

        for point in points:
            response = client.put(
                self.detail_url(point.id),
                json.dumps(data),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            # verify that the point was changed
            self.assertEquals(response.json()["label_text"], "Changed label")

    def test_admin_allow_delete(self):
        """Admins should be allowed to delete any userpoints they want."""
        client = self.get_client(self.admin_user)

        points = [
            UserPoint.objects.create(label_text="Foo", user=self.user),
            UserPoint.objects.create(label_text="Foo", user=self.admin_user),
            UserPoint.objects.create(label_text="Foo", user=None),
        ]

        for point in points:
            response = client.delete(
                self.detail_url(point.id),
            )
            self.assertEqual(response.status_code, 204)
            deleted_point = UserPoint.objects.filter(pk=point.id).first()
            self.assertIsNone(deleted_point)

    def test_anonymous_not_allow_update(self):
        """Shouldn't be allowed to update userpoints without login."""

        point = UserPoint.objects.create(label_text="Foo", user=self.admin_user)

        # unauthorized anonymous user
        client = self.get_client()

        data = {"label_text": "Changed label"}
        response = client.put(
            self.detail_url(point.id), json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)

    def test_anonymous_not_allow_delete(self):
        """Shouldn't be allowed to delete userpoints without login."""

        # unauthorized anonymous user
        point = UserPoint.objects.create(label_text="Foo", user=self.admin_user)
        client = self.get_client()

        response = client.delete(
            self.detail_url(point.id),
        )

        self.assertEqual(response.status_code, 401)
        # the point should still be there
        self.assertIsNotNone(UserPoint.objects.filter(pk=point.id).first())
