from rest_framework import serializers

from company_back.media.serializers import MediaSerializer
from company_back.models import Match, User


class MatchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "avatar", "firstName", "lastName"]
        read_only_fields = ["id, avatar", "firstName", "lastName"]

    def to_representation(self, instance):
        avatar = instance.avatar
        representation = super().to_representation(instance)
        representation["avatar"] = MediaSerializer(avatar).data["url"]

        return representation


class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"
        read_only_fields = ["id", "initiator", "reciever", "date"]

    def to_representation(self, instance):
        initiator = instance.initiator
        reciever = instance.reciever
        representation = super().to_representation(instance)
        representation["initiator"] = MatchUserSerializer(initiator).data
        representation["reciever"] = MatchUserSerializer(reciever).data
        return representation


class CreateMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"
        read_only_fields = ["id", "status", "date"]

    def to_representation(self, instance):
        initiator = instance.initiator
        reciever = instance.reciever
        representation = super().to_representation(instance)
        representation["initiator"] = MatchUserSerializer(initiator).data
        representation["reciever"] = MatchUserSerializer(reciever).data
        return representation
