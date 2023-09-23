from django.urls import include, path

urlpatterns = [
    path("auth/", include(("neobank.authentication.urls", "authentication"))),
    path("users/", include(("neobank.users.urls", "users"))),
]
