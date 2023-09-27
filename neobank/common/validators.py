from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from neobank.common import errors

class PhoneRegexValidator(RegexValidator):
    HELP_TEXT = _(
        "You must enter the telephone code, followed by a space and then the cell phone number. " "Ex: +57 3016789870"
    )

    def __init__(self):
        self.regex = "^[+]\d{1,5}(-\d{1,5})?\s(\d\s?)+$"
        self.message = self.HELP_TEXT
        super().__init__()


class BankAccountNumberValidator(RegexValidator):
    HELP_TEXT = errors.ACCOUNT_NUMBER_MUST_BE_TEN_DIGITS

    def __init__(self):
        self.regex = "^\d{10,}$"
        self.message = self.HELP_TEXT
        super().__init__()
