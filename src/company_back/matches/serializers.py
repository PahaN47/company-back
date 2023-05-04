from rest_framework import serializers

from company_back.models import Match


class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"
        read_only_fields = ["id", "initiator", "reciever", "date"]


class CreateMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"
        read_only_fields = ["id", "status", "date"]
