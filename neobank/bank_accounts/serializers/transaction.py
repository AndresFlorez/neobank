from django.db import models
from django.conf import settings
from rest_framework import serializers

from neobank.bank_accounts.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            "bank_account",
            "amount",
            "transaction_type",
        )