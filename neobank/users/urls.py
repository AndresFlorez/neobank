from django.urls import path

from .apis import UserSignUpApi, UserMeApi

urlpatterns = [
    path("", UserSignUpApi.as_view(), name="sign-up-api"),
    path("me/", UserMeApi.as_view(), name="me"),
]
