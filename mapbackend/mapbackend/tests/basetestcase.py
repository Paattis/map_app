from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.contrib.auth import get_user_model


class BaseTestCase(LiveServerTestCase):
  """Base class for all the test cases. Handles JWT access tokens and contains other convenience methods."""  
  fixtures = ["../fixtures/test_data.json"]

  def setUp(self):
    self.user = get_user_model().objects.get(pk=333)
    self.admin_user = get_user_model().objects.get(pk=222)
    pass

  def get_client(self, user:User=None):
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


  def get_access_token(self, user:User) -> Token:
    """Gets an access token for the given User

    Args:
        user (User):

    Returns:
        Token
    """    

    # TODO: GET FROM API WITH REQUEST
    token = RefreshToken.for_user(user)
    return token
