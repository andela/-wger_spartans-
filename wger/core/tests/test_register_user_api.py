from django.contrib.auth.models import User
from wger.core.tests.api_base_test import ApiPostTestCase, ApiBaseTestCase
from wger.core.tests.base_testcase import WorkoutManagerTestCase


class UserRegistrationTests(WorkoutManagerTestCase, ApiBaseTestCase, ApiPostTestCase):
    """
    Test the API endpoint for registration registration
    of users
    """
    resource = User
    private_resource = True
    special_endpoints = ()
    data = {'username': 'giddy254', 'password': 'password'}
