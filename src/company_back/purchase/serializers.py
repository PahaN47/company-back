from rest_framework import serializers

from company_back.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["status", "date"]
        extra_kwargs = {"balance": {"required": False}}
