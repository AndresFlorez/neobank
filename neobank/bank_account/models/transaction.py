from django.db import models
from django.conf import settings

class Transaction(BaseModel):

    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

    TYPE_CHOICES = (
        (DEPOSIT, DEPOSIT),
        (WITHDRAWAL, WITHDRAWAL),
    )

    bank_account = models.models.models.ForeignKey("neobank.BankAccount", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    transaction_type = models.CharField()
    # This should potentially be an encrypted field

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin
