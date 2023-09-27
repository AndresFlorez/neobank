from collections import abc
from django.db.models.query import QuerySet
from neobank.bank_accounts.models import BankAccount
from neobank.bank_accounts.filters import BankAccountFilter
from neobank.users.models import BaseUser


def bank_account_list(
    user: BaseUser = None,
    *,
    filters: abc.Mapping = None,
) -> QuerySet[BankAccount]:
    filters = filters or {}
    qs = BankAccount.objects.all()
    if user:
        qs = qs.filter(customer=user)
    return BankAccountFilter(filters, qs).qs
