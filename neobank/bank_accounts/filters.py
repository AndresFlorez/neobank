import django_filters

from neobank.bank_accounts.models import BankAccount

class BankAccountFilter(django_filters.FilterSet):
    class Meta:
        model = BankAccount
        fields = ("account_number", "customer")
