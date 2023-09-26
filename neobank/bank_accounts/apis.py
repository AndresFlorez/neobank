from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from neobank.api.mixins import ApiAuthMixin
from neobank.bank_accounts.models import BankAccount
from neobank.bank_accounts.serializers import BankAccountSerializer, BankAccountDetailSerializer


class BankAccountCreateApi(ApiAuthMixin, APIView):
    queryset = BankAccount.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = BankAccountSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        bank_accounts = BankAccount.objects.all()
        serializer = BankAccountDetailSerializer(bank_accounts, many=True)
        return Response(serializer.data)
