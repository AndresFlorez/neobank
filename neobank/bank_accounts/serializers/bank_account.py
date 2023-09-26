from rest_framework import serializers
from neobank.bank_accounts.models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BankAccount
        fields = (
            "account_number",
            "balance",
            "customer",
        )


class BankAccountDetailSerializer(serializers.ModelSerializer):
    pass
