from django.contrib.auth import get_user_model
from rest_framework import serializers

from neobank.users.models import UserProfile
from .user_profile import UserProfileSerializer

class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(many=False)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "user_profile"
        )
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("id",)

    def create(self, validated_data):
        # set password
        user_profile_data = validated_data["user_profile"]
        del validated_data["user_profile"]
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        user_profile = UserProfile(user=instance)
        user_profile_serializer = UserProfileSerializer(
            instance=user_profile, data=user_profile_data, partial=True
        )

        if user_profile_serializer.is_valid():
            user_profile_serializer.save()

        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
