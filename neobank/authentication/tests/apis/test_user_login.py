from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from neobank.users.models import BaseUser
from neobank.users.services import user_create


class UserJwtLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.jwt_login_url = reverse("v1:authentication:jwt:login")
        self.jwt_logout_url = reverse("v1:authentication:jwt:logout")
        self.me_url = reverse("v1:users:me")

    def test_non_existing_user_cannot_login(self):
        self.assertEqual(0, BaseUser.objects.count())

        data = {"email": "test@test.com", "password": "hacksoft"}

        response = self.client.post(self.jwt_login_url, data)

        self.assertEqual(400, response.status_code)

    def test_existing_user_can_login_and_access_apis(self):
        """
        1. Create user
        2. Assert login is OK
        3. Call /v1/auth/me
        4. Assert valid response
        """
        credentials = {"email": "test@test.com", "password": "password"}

        user_create(**credentials)

        response = self.client.post(self.jwt_login_url, credentials)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertIn("token", data)
        token = data["token"]

        jwt_cookie = response.cookies.get(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        self.assertEqual(token, jwt_cookie.value)

        response = self.client.get(self.me_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Now, try without session attached to the client
        client = APIClient()

        response = client.get(self.me_url)
        self.assertEqual(403, response.status_code)

        auth_headers = {"HTTP_AUTHORIZATION": f"{settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX']} {token}"}
        response = client.get(self.me_url, **auth_headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_existing_user_can_logout(self):
        """
        1. Create user
        2. Login, can access APIs
        3. Logout, cannot access APIs
        """
        credentials = {"email": "test@test.com", "password": "password"}

        user = user_create(**credentials)

        key_before_logout = user.jwt_key

        response = self.client.post(self.jwt_login_url, credentials)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.get(self.me_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.client.post(self.jwt_logout_url)

        response = self.client.get(self.me_url)
        self.assertEqual(403, response.status_code)

        user.refresh_from_db()
        key_after_logout = user.jwt_key

        self.assertNotEqual(key_before_logout, key_after_logout)
