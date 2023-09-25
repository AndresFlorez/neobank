from django.db import models
from django.conf import settings

class BankAccount(BaseModel):
    account_number = models.models.CharField(max_length=50)
    balance = models.FloatField(default=0)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.account_number
