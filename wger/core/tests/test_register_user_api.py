from django.contrib.auth.models import User
from wger.core.tests.api_base_test import ApiPostTestCase, ApiBaseTestCase
from wger.core.tests.base_testcase import WorkoutManagerTestCase


class ApiUserRegistrationTests(WorkoutManagerTestCase, ApiBaseTestCase, ApiPostTestCase):
    """
    Test the API endpoint for registration registration
    of users
    """
    url = '/api/v2/user/register/'
    url_detail = '/api/v2/user/register/1/'
    resource = User
    private_resource = True
    special_endpoints = ()
    data = {'username': 'giddy254', 'email': 'giddy@example.com', 'password': 'password'}
