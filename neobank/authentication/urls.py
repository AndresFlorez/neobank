from django.urls import include, path

from .apis import (
    UserJwtLoginApi,
    UserJwtLogoutApi,
)

urlpatterns = [
    path(
        "jwt/",
        include(
            (
                [
                    path("login/", UserJwtLoginApi.as_view(), name="login"),
                    path("logout/", UserJwtLogoutApi.as_view(), name="logout"),
                ],
                "jwt",
            )
        ),
    ),
]
