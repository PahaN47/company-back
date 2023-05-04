from rest_framework import serializers

from company_back.gifts.serializers import GiftsSerializer
from company_back.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["status", "date"]
        extra_kwargs = {"balance": {"required": False}}


class RecievedGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ["gift"]
        read_only_fields = ["gift"]

    def to_representation(self, instance):
        gift = instance.gift
        return GiftsSerializer().to_representation(gift)
