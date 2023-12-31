from django.core.exceptions import ValidationError
from django.test import TestCase

from neobank.users.models import BaseUser
from neobank.users.services import user_create


class UserCreateTests(TestCase):
    def test_user_without_password_is_created_with_unusable_one(self):
        user = user_create(email="test@test.com")

        self.assertFalse(user.has_usable_password())

    def test_user_with_capitalized_email_cannot_be_created(self):
        user_create(email="test@test.com")

        with self.assertRaises(ValidationError):
            user_create(email="TEST@test.com")

        self.assertEqual(1, BaseUser.objects.count())
