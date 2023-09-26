from django.urls import path

from .apis import BankAccountCreateApi

urlpatterns = [path("", BankAccountCreateApi.as_view(), name="create-bank-account-api")]
