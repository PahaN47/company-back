from rest_framework import serializers

from company_back.countries.serializers import CountrySerializer
from company_back.media.serializers import MediaSerializer
from company_back.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "firstName", "avatar", "age", "gender", "country"]
        read_only_fields = ["id", "firstName", "avatar", "age", "gender", "country"]

    def to_representation(self, instance):
        country = instance.country
        avatar = instance.avatar
        representation = super().to_representation(instance)
        representation["country"] = CountrySerializer(country).data
        representation["avatar"] = MediaSerializer(avatar).data["url"]

        return representation
