from django.db import models
from django.conf import settings
from neobank.common.models import BaseModel


class BankAccount(BaseModel):
    account_number = models.CharField(max_length=50, unique=True)
    balance = models.FloatField(default=0)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.account_number
