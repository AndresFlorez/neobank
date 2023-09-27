from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from neobank.api.mixins import ApiAuthMixin
from neobank.bank_accounts.models import BankAccount
from neobank.bank_accounts.serializers import (
    BankAccountSerializer,
    BankAccountDetailSerializer,
    TransactionSerializer,
)
from neobank.bank_accounts.services import BankAccountTransactionService
from neobank.bank_accounts.selectors import bank_account_list


class BankAccountListCreateApi(ApiAuthMixin, generics.ListCreateAPIView):
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        user = self.request.user
        return bank_account_list(user, filters=self.request.query_params)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BankAccountSerializer
        else:
            return BankAccountDetailSerializer


class TransactionCreateApi(ApiAuthMixin, generics.GenericAPIView):
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        BankAccountTransactionService(
            transaction=instance,
        ).apply_transaction_to_bank_account()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
