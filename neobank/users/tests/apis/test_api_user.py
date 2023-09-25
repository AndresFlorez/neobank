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
        # reverse("v1:authentication:jwt:login")
        self.user_sign_up_url = reverse("v1:users:sign-up-api")

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
                "identification": "1144059543"
            }
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
                "identification": "1144059543"
            }
        }

        response = self.client.post(self.user_sign_up_url, data, format="json")
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_data["detail"]["email"][0],
            "base user with this email address already exists."
        )
