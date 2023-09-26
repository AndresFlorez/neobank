from django.db import models
from neobank.common.models import BaseModel


class Transaction(BaseModel):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

    TYPE_CHOICES = (
        (DEPOSIT, DEPOSIT),
        (WITHDRAWAL, WITHDRAWAL),
    )

    bank_account = models.ForeignKey("bank_accounts.BankAccount", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    transaction_type = models.CharField()
