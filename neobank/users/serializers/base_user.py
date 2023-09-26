from django.contrib.auth import get_user_model
from rest_framework import serializers

from neobank.users.models import UserProfile
from .user_profile import UserProfileSerializer
from neobank.users.services import create_user_profile


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(many=False)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "password", "user_profile")
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("id",)

    def create(self, validated_data):
        user_profile_data = validated_data["user_profile"]
        del validated_data["user_profile"]
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        # set password
        if password is not None:
            instance.set_password(password)
        instance.save()

        create_user_profile(instance, user_profile_data)

        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
