from rest_framework import serializers
from company_back.media.serializers import MediaSerializer

from company_back.models import Chat, User


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "firstName", "lastName", "avatar"]
        read_only_fields = ["id", "firstName", "lastName", "avatar"]

    def to_representation(self, instance):
        avatar = instance.avatar
        representation = super().to_representation(instance)
        representation["avatar"] = MediaSerializer(avatar).data["url"]
        return super().to_representation(instance)


class ChatsSerializer(serializers.ModelSerializer):
    user1 = ChatUserSerializer(read_only=True, many=False)
    user2 = ChatUserSerializer(read_only=True, many=False)

    class Meta:
        model = Chat
        fields = "__all__"
