from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from neobank.bank_accounts.models import Transaction
from neobank.common import errors


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(min_value=1)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "bank_account",
            "amount",
            "transaction_type",
            "created_at",
        )
        read_only_fields = ("created_at",)

    def validate_bank_account(self, value):
        if value.customer != self.context["request"].user:
            raise serializers.ValidationError(errors.INVALID_BANK_ACCOUNT_USER)
        return value

    def validate(self, data):
        # validate that bank account has balance
        if (
            not data.get("bank_account").balance >= data.get("amount", 0)
            and data.get("transaction_type") == Transaction.WITHDRAWAL
        ):
            raise serializers.ValidationError({"amount": [errors.NOT_ENOUGH_BALANCE]})

        return data
