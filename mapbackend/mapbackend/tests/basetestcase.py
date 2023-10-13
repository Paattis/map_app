from django.test import LiveServerTestCase
from django.test import Client
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, Token

class BaseTestCase(LiveServerTestCase):
  fixtures = ["../fixtures/test_data.json"]
  
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
