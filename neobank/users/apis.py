from django.conf import settings
from rest_framework import serializers
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings

from neobank.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from neobank.users.models import BaseUser
from neobank.users.selectors import user_list
from neobank.users.serializers import UserSerializer, UserProfileSerializer


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSignUpApi(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        
        # Set token as a cookie
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.set_cookie(settings.JWT_AUTH_COOKIE, token)  # Set cookie
        return response
