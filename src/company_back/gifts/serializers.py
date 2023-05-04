from rest_framework import serializers
from company_back.media.serializers import MediaSerializer

from company_back.models import Gift


class GiftsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = "__all__"

    def to_representation(self, instance):
        image = instance.image
        representation = super().to_representation(instance)
        representation["image"] = MediaSerializer(image).data["url"]

        return representation
