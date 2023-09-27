from django.core.exceptions import ValidationError
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from neobank.users.models import BaseUser
from neobank.users.services import user_create


class UserAPiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_sign_up_url = reverse("v1:users:sign-up-api")
        self.jwt_login_url = reverse("v1:authentication:jwt:login")
        self.me_url = reverse("v1:users:me")

    def test_user_sign_up_correct_register(self):
        data = {
            "email": "tes6@test.com",
            "first_name": "Andres",
            "last_name": "Florez",
            "password": "DeV.2023",
            "user_profile": {
                "country": "colombia",
                "address": "calle 18a",
                "telephone": "+57 3104427917",
                "identification": "1144059543",
            },
        }

        response = self.client.post(self.user_sign_up_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(settings.JWT_AUTH_COOKIE, response.cookies)

    def test_user_sign_up_email_already_exists(self):
        user_create(email="test@test.com")

        data = {
            "email": "test@test.com",
            "first_name": "Andres",
            "last_name": "Florez",
            "password": "DeV.2023",
            "user_profile": {
                "country": "colombia",
                "address": "calle 18a",
                "telephone": "+57 3104427917",
                "identification": "1144059543",
            },
        }

        response = self.client.post(self.user_sign_up_url, data, format="json")
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_data["extra"]["fields"]["email"][0], "base user with this email address already exists."
        )

    def test_me_api(self):
        """
        Validate endpoint for get logged user information.
        """
        credentials = {"email": "test@test.com", "password": "password"}

        user = user_create(**credentials)

        response = self.client.post(self.jwt_login_url, credentials)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.me_url)
        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual(response_data.get("email"), user.email)
        self.assertTrue(response_data.get("is_active"))
        self.assertFalse(response_data.get("is_admin"))
        self.assertFalse(response_data.get("is_superuser"))
