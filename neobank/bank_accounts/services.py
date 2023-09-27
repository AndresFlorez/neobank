import operator

from typing import Any
from neobank.bank_accounts.models import Transaction
from django.utils.translation import gettext_lazy as _


class BankAccountTransactionService:
    operations = {
        Transaction.DEPOSIT: operator.add,
        Transaction.WITHDRAWAL: operator.sub,
    }

    def __init__(self, transaction: Transaction):
        self.transaction = transaction
        self.bank_account = transaction.bank_account

    def apply_transaction_to_bank_account(self):
        transaction_type_function = self.operations.get(self.transaction.transaction_type)
        self.bank_account.balance = transaction_type_function(
            self.bank_account.balance,
            self.transaction.amount,
        )
        self.bank_account.save()
