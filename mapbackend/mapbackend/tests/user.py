from django.test import TestCase
from django.urls import reverse
import json
from mapbackend.tests import BaseTestCase
from django.contrib.auth import get_user_model
from points.models import UserPoint
from rest_framework.test import APIClient


class UserTests(BaseTestCase):
    """Test cases concerning everything relating to Users (tokens, logins, user creation etc.)
    """
    list_view_name = "api:user-list"
    detail_view_name = "api:user-detail"

    def test_user_should_only_see_own_data(self):
        """non-admin users should only be able to view their own data from the /users/ endpoint"""
        client = self.get_client(self.user)
        response = client.get(self.list_url)

        self.assertEqual(response.status_code, 200)

        expected_data = [
            {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email
            }
        ]
        # list operation should only return the currently logged in user
        self.assertEqual(response.json(), expected_data)

        # fetch an id for a user that isn't the currently logged in one
        other_user_id = get_user_model().objects.exclude(pk=self.user.id).first().id

        response = client.get(self.detail_url(other_user_id))

        # shouldn't be able to fetch data for users that aren't the currently logged in one
        self.assertEqual(response.status_code, 404)

        # should allow to fetch the data for the currently logged in user
        response = client.get(self.detail_url(self.user.id))
        self.assertEqual(response.status_code, 200)

    def test_user_should_only_update_own_data(self):
        """Regular users should only be allowed to update their own user data"""
        client = self.get_client(self.user)

        data = {"username": "changed_username"}
        expected_data = {
            "id": self.user.id,
            "username": data["username"],
            "email": self.user.email
        }

        response = client.put(
            self.detail_url(self.user.id),
            json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        # the data should have been changed
        self.assertEqual(response.json(), expected_data)
        pass

    def test_admin_should_view_every_user(self):
        """Admin users should be allowed to list and retrieve all user data through the /users/ endpoint"""
        client = self.get_client(self.admin_user)
        response = client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        # see how many user objects got returned, compare to the actual count in database
        response_user_count = len(response.json())
        db_user_count = get_user_model().objects.count()

        # they should be equal as the admins can list every user
        self.assertEqual(response_user_count, db_user_count)

        # get user with a different id than the current one
        other_user = get_user_model().objects.exclude(pk=self.admin_user.id).first()
        response = client.get(self.detail_url(other_user.id))

        self.assertEqual(response.status_code, 200)

        expected_data = {
            "username": other_user.username,
            "email": other_user.email,
            "id": other_user.id
        }

        # verify that the correct user was fetched
        self.assertEqual(response.json(), expected_data)

    def test_can_get_jwt_token(self):
        """The `/token/` endpoint should return the appropriate JWT tokens when 
        given the correct user credentials"""
        client = self.get_client()
        data = {"username": "Martin Mapper", "password": "password"}
        response = client.post(reverse("token_obtain_pair"), json.dumps(data),
                               content_type="application/json")

        # get access and refresh tokens, assert them
        self.assertEqual(response.status_code, 200)

        access_token = response.json().get("access")
        refresh_token = response.json().get("refresh")
        self.assertIsNotNone(access_token)
        self.assertIsNotNone(refresh_token)

        # verify the tokens via the token verification endpoint
        for token in [access_token, refresh_token]:
            response = client.post(
                reverse("token_verify"),
                json.dumps({"token": token}),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
