from rest_framework import serializers

from neobank.users.models.user_profile import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "identification",
            "telephone",
            "address",
            "country",
        )
