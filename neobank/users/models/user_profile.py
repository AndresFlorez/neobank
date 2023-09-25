import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager as BUM
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings

from neobank.common.models import BaseModel
from neobank.common.validators import PhoneRegexValidator

# Taken from here:
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
# With some modifications
User = settings.AUTH_USER_MODEL

class UserProfile(BaseModel):

    identification = models.CharField(max_length=100, blank=True, null=True, db_index=True)

    telephone = models.CharField(
        max_length=100,
        blank=True,
        validators=[PhoneRegexValidator()],
        help_text=PhoneRegexValidator.HELP_TEXT,
    )

    address = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='user_profile',
    )

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)
