from collections import abc

from django.db import transaction

from neobank.common.services import model_update
from neobank.users.models import BaseUser, UserProfile


def user_create(*, email: str, is_active: bool = True, is_admin: bool = False, password: str | None = None) -> BaseUser:
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
