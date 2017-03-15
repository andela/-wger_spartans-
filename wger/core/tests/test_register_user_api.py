from django.contrib.auth.models import User
from wger.core.tests.api_base_test import ApiPostTestCase



class UserRegistrationTests(ApiPostTestCase):
    """
    Test the API endpoint for registration registration
    of users
    """
    resource = User
    url = '/api/v2/user/registration/'
    data = {'username': 'giddy254', 'password': 'password'}

