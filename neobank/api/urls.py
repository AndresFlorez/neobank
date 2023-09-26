from django.urls import include, path

urlpatterns = [
    path("auth/", include(("neobank.authentication.urls", "authentication"))),
    path("users/", include(("neobank.users.urls", "users"))),
    path("banck_accounts/", include(("neobank.bank_accounts.urls", "bank_accounts"))),
]
