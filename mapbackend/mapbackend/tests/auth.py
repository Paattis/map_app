from django.test import TestCase

import json
from mapbackend.tests import BaseTestCase
from django.contrib.auth import get_user_model
from points.models import UserPoint


class AuthTests(BaseTestCase):
    """Test cases concerning everything relating to authorization (tokens, logins, user creation etc.)
    """
    list_view_name = "api:user-list"
    detail_view_name = "api:user-detail"

    def test_can_get_jwt_token(self):
        """The `/token/` endpoint should return the appropriate JWT tokens when 
        given the correct user credentials"""
        client = self.get_client()
        data = {"username": "Martin Mapper", "password": "password"}
        response = client.post(self.list_url, json.dumps(data),
                               content_type="application/json")
