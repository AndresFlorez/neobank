from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django_dynamic_fixture import G

from neobank.bank_accounts.models import BankAccount, Transaction
from neobank.users.services import user_create
from neobank.common import errors


class BankAccountApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_create(email="test@test.com", password="password")
        self.user2 = user_create(email="test2@test.com", password="password")

        self.bank_account_create_list_url = reverse("v1:bank_accounts:create-bank-account-api")
        self.bank_account_transactions_url = reverse("v1:bank_accounts:create-transaction-api")

        self.account_number = "0123456789"
        self.initial_amount = 1000000
        self.debit_amount = 500000
        self.bank_account_payload = {"account_number": self.account_number}
        self.transaction_payload = {
            "bank_account": self.account_number,
            "transaction_type": Transaction.DEPOSIT,
            "amount": self.initial_amount,
        }

        self.__login__()

    def __login__(self):
        self.client.force_authenticate(self.user)

    def test_create_bank_account(self):
        response = self.client.post(
            self.bank_account_create_list_url,
            self.bank_account_payload,
            format="multipart",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data.get("account_number"), self.account_number)
        self.assertEqual(response_data.get("balance"), 0)

    def test_create_transactions(self):
        """
        Create DEPOSIT and WITHDRAWAL
        1. Create bank account
        2. Create transaction of type deposit
        3. Create transaction of type withdrawal
        4. Validate bank account
        """
        G(BankAccount, account_number=self.account_number, customer=self.user)

        # DEPOSIT
        response = self.client.post(
            self.bank_account_transactions_url,
            self.transaction_payload,
            format="multipart",
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data.get("bank_account"), self.account_number)
        self.assertEqual(response_data.get("amount"), self.initial_amount)

        # WITHDRAWAL
        self.transaction_payload["transaction_type"] = Transaction.WITHDRAWAL
        self.transaction_payload["amount"] = self.debit_amount
        response = self.client.post(
            self.bank_account_transactions_url,
            self.transaction_payload,
            format="multipart",
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data.get("bank_account"), self.account_number)
        self.assertEqual(response_data.get("amount"), self.debit_amount)

        # GET BANK ACCOUNT
        response = self.client.get(
            self.bank_account_create_list_url,
            format="multipart",
        )
        response_data = response.json()

        bank_account_data = response_data[0]
        new_balance = self.initial_amount - self.debit_amount

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bank_account_data.get("account_number"), self.account_number)
        self.assertEqual(bank_account_data.get("balance"), new_balance)
        self.assertEqual(len(bank_account_data.get("transactions")), 2)

    def test_create_transactions_with_amount_zero(self):
        """
        1. Create bank account
        2. Create transaction of type deposit with amount = 0
        """
        G(BankAccount, account_number=self.account_number, customer=self.user)

        # DEPOSIT
        self.transaction_payload["amount"] = 0
        response = self.client.post(
            self.bank_account_transactions_url,
            self.transaction_payload,
            format="multipart",
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_data["extra"]["fields"]["amount"][0],
            "Ensure this value is greater than or equal to 1.",
        )

    def test_create_bank_account_without_login(self):
        self.client.logout()

        response = self.client.post(
            self.bank_account_create_list_url,
            self.bank_account_payload,
            format="multipart",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response_data.get("message"),
            "Authentication credentials were not provided.",
        )

    def test_create_bank_account_account_number_already_exists(self):
        G(BankAccount, account_number=self.account_number)

        response = self.client.post(
            self.bank_account_create_list_url,
            self.bank_account_payload,
            format="multipart",
        )

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response_data.get("message"), "Validation error")
        self.assertEqual(
            response_data["extra"]["fields"]["account_number"][0],
            "bank account with this account number already exists.",
        )

    def test_create_transaction_with_insufficient_balance(self):
        G(BankAccount, account_number=self.account_number, customer=self.user)
        self.transaction_payload["transaction_type"] = Transaction.WITHDRAWAL
        response = self.client.post(
            self.bank_account_transactions_url,
            self.transaction_payload,
            format="multipart",
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response_data.get("message"), "Validation error")
        self.assertEqual(
            response_data["extra"]["fields"]["amount"][0],
            errors.NOT_ENOUGH_BALANCE,
        )

    def test_create_bank_account_invalid_lengh_account_number(self):
        """
        Max lengh is 10.
        """
        self.bank_account_payload["account_number"] = "01234567890"
        response = self.client.post(
            self.bank_account_create_list_url,
            self.bank_account_payload,
            format="multipart",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_data["extra"]["fields"]["account_number"][0],
            "Ensure this field has no more than 10 characters.",
        )

    def test_create_bank_account_invalid_char_account_number(self):
        """
        account_number only accepts numbers
        """
        self.bank_account_payload["account_number"] = "A123456789"
        response = self.client.post(
            self.bank_account_create_list_url,
            self.bank_account_payload,
            format="multipart",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_data["extra"]["fields"]["account_number"][0],
            errors.ACCOUNT_NUMBER_MUST_BE_TEN_DIGITS,
        )

    def test_get_only_one_bank_account(self):
        G(BankAccount, account_number="0123456789", customer=self.user)
        G(BankAccount, account_number="9876543210", customer=self.user)

        response = self.client.get(
            self.bank_account_create_list_url,
            format="multipart",
        )
        response_data = response.json()
        self.assertEqual(len(response_data), 2)

        url = self.bank_account_create_list_url + "?account_number=0123456789"
        response = self.client.get(
            url,
            format="multipart",
        )
        response_data = response.json()

        self.assertEqual(len(response_data), 1)
