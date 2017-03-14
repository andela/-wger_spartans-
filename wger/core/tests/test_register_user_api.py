from django.contrib.auth.models import User
from wger.core.tests.base_testcase import WorkoutManagerTestCase


class UserRegistrationTests(WorkoutManagerTestCase):
    """
    Test the API endpoint for registration registration
    of users
    """

    def test_registration_endpoint(self):
        # Test for user registration
        url = '/api/v2/user/registration/'
        data = {'username': 'giddy254', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
