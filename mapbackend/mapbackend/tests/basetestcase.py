from django.test import LiveServerTestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.contrib.auth import get_user_model
from django.db import models


class BaseTestCase(LiveServerTestCase):
    """Base class for all the test cases. Handles JWT access tokens and contains other convenience methods."""

    fixtures = ["../fixtures/test_data.json"]
    list_view_name: str
    detail_view_name: str

    def setUp(self):
        self.user = get_user_model().objects.get(pk=333)
        self.admin_user = get_user_model().objects.get(pk=222)
        self.list_url = reverse(self.list_view_name)
        pass

    def assert_exists(self, model: models.Model, pk: int) -> bool:
        """Shorthand for asserting that an object with a given pk exists in a table."""
        return self.assertIsNotNone(model.objects.filter(pk=pk).first())

    def assert_deleted(self, model: models.Model, pk: int) -> bool:
        """Shorthand for asserting that an object was deleted from the database."""
        return self.assertIsNone(model.objects.filter(pk=pk).first())

    def detail_url(self, pk: int) -> str:
        """Convenience Wrapper for django.urls.reverse to save space in source code.
            Returns the detail url for a singular item (e.g. /users/123/).
        Args:
            pk (int): the primary key of the object you want a link to

        Returns:
            str: the url
        """
        return reverse(self.detail_view_name, kwargs={"pk": pk})

    def get_client(self, user: User = None) -> APIClient:
        """Gets a new client object. Sets up JWT auth if a User is supplied.

        Args:
            user (User, optional): The User to set up the JWT auth for. Defaults to None.
        """
        client = APIClient()
        if not user:
            return client

        token = self.get_access_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        return client

    def get_access_token(self, user: User) -> Token:
        """Gets an access token for the given User

        Args:
            user (User): the User to get the token for

        Returns:
            Token
        """

        token = RefreshToken.for_user(user)
        return token
