from django.db import models
from django.conf import settings

from neobank.common.models import BaseModel
from neobank.common.validators import BankAccountNumberValidator


class BankAccount(BaseModel):
    account_number = models.CharField(
        primary_key=True,
        max_length=10,
        unique=True,
        validators=[BankAccountNumberValidator()],
        help_text=BankAccountNumberValidator.HELP_TEXT,
    )
    balance = models.FloatField(default=0)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.account_number
