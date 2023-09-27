from django.urls import path

from .apis import BankAccountListCreateApi, TransactionCreateApi

urlpatterns = [
    path("", BankAccountListCreateApi.as_view(), name="create-bank-account-api"),
    path("transactions/", TransactionCreateApi.as_view(), name="create-transaction-api"),
]
