from django.test import TestCase
from django.urls import reverse
import json
from mapbackend.tests import BaseTestCase
from django.contrib.auth import get_user_model
from points.models import UserPoint
from rest_framework.test import APIClient


class UserTests(BaseTestCase):
    """Test cases concerning everything relating to Users (tokens, logins, user creation etc.)"""

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
                "email": self.user.email,
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
            "email": self.user.email,
        }

        response = client.put(
            self.detail_url(self.user.id),
            json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        # the data should have been changed
        self.assertEqual(response.json(), expected_data)
        pass

    def test_admin_should_update_all_data(self):
        """Admins should be allowed to update any user's data"""
        client = self.get_client(self.admin_user)

        data = {"username": "changed_username"}

        user_to_modify = get_user_model().objects.exclude(pk=self.admin_user.id).first()

        expected_data = {
            "id": self.user.id,
            "username": data["username"],
            "email": self.user.email,
        }

        response = client.put(
            self.detail_url(user_to_modify.id),
            json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        # the data should have been changed
        self.assertEqual(response.json(), expected_data)
        pass

    def test_admin_should_be_able_to_view_every_user(self):
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
            "id": other_user.id,
        }

        # verify that the correct user was fetched
        self.assertEqual(response.json(), expected_data)

    def test_admin_can_delete_any_user(self):
        """Admins should be able to delete any user"""
        user_to_delete = get_user_model().objects.create(
            username="deletable", email="toBeDeleted@mail.com"
        )

        client = self.get_client(self.admin_user)
        response = client.delete(self.detail_url(user_to_delete.id))

        self.assertEqual(response.status_code, 204)

        # check that user actually got deleted in the database
        print("usertodelete id", user_to_delete.id)
        self.assert_deleted(get_user_model(), user_to_delete.id)

    def test_user_can_delete_own_user(self):
        """Regular users should be able to delete their own user but not other users."""
        user_to_delete = get_user_model().objects.create(
            username="toBeDeleted", email="toBeDeleted@mail.com"
        )

        should_not_be_deleted = get_user_model().objects.create(
            username="ShouldNotBeDeleted", email="ShouldNotBeDeleted@mail.com"
        )

        client = self.get_client(user_to_delete)
        # shouldnt be able to delete an other user's data
        response = client.delete(self.detail_url(should_not_be_deleted.id))
        self.assertEqual(response.status_code, 404)
        self.assert_exists(get_user_model(), should_not_be_deleted.id)

        # should be able to delete their own data
        response = client.delete(self.detail_url(user_to_delete.id))
        self.assertEqual(response.status_code, 204)
        self.assert_deleted(get_user_model(), user_to_delete.id)

    def test_can_register_new_user_with_valid_data(self):
        """User registration should work with valid data"""
        client = self.get_client()
        data = {
            "username": "New user",
            "email": "newuser@mail.com",
            "password": "Tops3cr3t123",
            "password2": "Tops3cr3t123",
        }

        response = client.post(
            reverse("register_user"), json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        new_user = get_user_model().objects.last()
        expected_data = {
            "username": new_user.username,
            "email": new_user.email,
            "id": new_user.id,
        }

        self.assertEqual(response.json(), expected_data)

    def test_cannot_register_new_user_with_invalid_data(self):
        """User registration should not work with invalid data"""
        client = self.get_client()

        # invalid user data
        # autopep8: off
        test_data = [
            {
                "username": "BadEmail",
                "email": "newuser",
                "password": "Tops3cr3t123",
                "password2": "Tops3cr3t123",
            },
            {
                "username": "DiffPasswords",
                "email": "newuser@mail.com",
                "password": "Tops3cr3t12",
                "password2": "D1ff3rentp4ssword",
            },
            {
                "username": "",
                "email": "BlankUserName@mail.com",
                "password": "Tops3cr3t123",
                "password2": "Tops3cr3t123",
            },
            {
                "email": "NoUserName@mail.com",
                "password": "Tops3cr3t123",
                "password2": "Tops3cr3t123",
            },
            {
                "username": "Martin Mapper",
                "email": "email@mail.com",
                "password": "Tops3cr3t123",
                "password2": "Tops3cr3t123",
            },
            {
                "username": "Martin Mailer",
                "email": "Martin@mail.com",
                "password": "Tops3cr3t123",
                "password2": "Tops3cr3t123",
            },
        ]
        # autopep8: on

        for data in test_data:
            response = client.post(
                reverse("register_user"),
                json.dumps(data),
                content_type="application/json",
            )

            self.assertEqual(response.status_code, 400)

    def test_can_get_jwt_token(self):
        """The `/token/` endpoint should return the appropriate JWT tokens when
        given the correct user credentials"""
        client = self.get_client()
        data = {"username": "Martin Mapper", "password": "password"}
        response = client.post(
            reverse("token_obtain_pair"),
            json.dumps(data),
            content_type="application/json",
        )

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
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
