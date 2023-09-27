from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from neobank.api.mixins import ApiAuthMixin
from neobank.users.models import BaseUser
from neobank.users.serializers import UserSerializer
from neobank.users.selectors import user_get_login_data
from neobank.users.services import generate_response_with_token



class UserSignUpApi(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Create an user and set cookie on response (login)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return generate_response_with_token(user, serializer.data)


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)
        return Response(data)
