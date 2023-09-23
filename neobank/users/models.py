import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

from neobank.common.models import BaseModel
from neobank.common.validators import PhoneRegexValidator

# Taken from here:
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
# With some modifications


class BaseUserManager(BUM):
    def create_user(self, email, is_active=True, is_admin=False, password=None, first_name : str = None, last_name : str = None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            is_admin=is_admin,
            first_name=first_name,
            last_name=last_name
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email : str, password : str = None, first_name : str = None, last_name : str = None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
            first_name=first_name,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    # This should potentially be an encrypted field
    jwt_key = models.UUIDField(default=uuid.uuid4)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin

class UserProfile(BaseModel):

    identification = models.CharField(max_length=100, blank=True, null=True, db_index=True)

    telephone = models.CharField(
        max_length=100,
        blank=True,
        validators=[PhoneRegexValidator()],
        help_text=PhoneRegexValidator.HELP_TEXT,
        verbose_name=_('Cell phone number'),
    )

    address = models.CharField(max_length=100, blank=True)

    country = models.CharField(max_length=100, blank=True)


    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name='user_profile',
        related_name='user_profile',
    )

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)

    @property
    def has_digital_certificate(self):
        if self.certificate_set.all():
            return True
        else:
            return False

    def get_user_profile_by_tin(user_tin):
        user_profile = UserProfile.objects.get(tax_number=user_tin)
        return user_profile
