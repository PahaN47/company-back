from django.core.validators import EmailValidator

from rest_framework import serializers

from company_back.countries.serializers import CountrySerializer
from company_back.media.serializers import MediaSerializer
from company_back.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "firstName",
            "lastName",
            "phone",
            "email",
            "avatar",
            "gender",
            "birthDate",
            "country",
            "timezone",
        ]

        read_only_fields = ["id"]
        extra_kwargs = {"email": {"validators": [EmailValidator]}}

    def to_representation(self, instance):
        country = instance.country
        avater = instance.avatar
        representation = super().to_representation(instance)
        representation["country"] = CountrySerializer(country).data
        representation["avatar"] = MediaSerializer(avater).data["url"]

        return representation
