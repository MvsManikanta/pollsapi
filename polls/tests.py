from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from polls import apiviews
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class TestPoll(APITestCase):
    def setUp(self):
        # Create test user
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)

        # Authenticated client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Request factory and view
        self.factory = APIRequestFactory()
        self.view = apiviews.PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            username='test',
            email='testuser@test.com',
            password='test'
        )

    def test_create_poll(self):
        params = {
            "question": "How are you?",
            "created_by": self.user.id
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201,
                         f"Expected 201, got {response.status_code}")

    def test_list_polls_with_client(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,
                         f"Expected 200, got {response.status_code}")

    def test_list_polls_with_factory(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         f"Expected 200, got {response.status_code}")
    def test_create(self):
        self.client.login(username="test", password="test")
        params = {
            "question": "How are you?",
            "created_by": 1
            }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201,
                        'Expected Response Code 201, received {0} instead.'
                        .format(response.status_code))
