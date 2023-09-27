from rest_framework import serializers
from neobank.bank_accounts.models import BankAccount
from .transaction import TransactionSerializer


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
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = BankAccount
        fields = (
            "account_number",
            "balance",
            "customer",
            "transactions",
        )
