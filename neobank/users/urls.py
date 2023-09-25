from django.urls import path

from .apis import UserSignUpApi

urlpatterns = [path("", UserSignUpApi.as_view(), name="sign-up-api")]
