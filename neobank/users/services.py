from collections import abc

from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import set_cookie_with_token
from rest_framework.response import Response
from django.http import HttpResponse

from neobank.common.services import model_update
from neobank.users.models import BaseUser, UserProfile


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def user_create(
    *,
    email: str,
    is_active: bool = True,
    is_admin: bool = False,
    password: str | None = None,
) -> BaseUser:
    user = BaseUser.objects.create_user(email=email, is_active=is_active, is_admin=is_admin, password=password)

    return user


@transaction.atomic
def user_update(*, user: BaseUser, data: abc.Mapping) -> BaseUser:
    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    return user


@transaction.atomic
def create_user_profile(user: BaseUser, user_profile_data: abc.Mapping) -> UserProfile:
    user_profile = UserProfile(user=user, **user_profile_data)
    user_profile.save()
    return user_profile


def generate_response_with_token(user: BaseUser, data: abc.Mapping) -> HttpResponse:
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    # Set token as a cookie
    response = Response(data, status=status.HTTP_201_CREATED)
    set_cookie_with_token(response, settings.JWT_AUTH_COOKIE, token)  # Set cookie
    return response
