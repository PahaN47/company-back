from rest_framework import serializers
from company_back.media.serializers import MediaSerializer

from company_back.models import Chat, User


class ChatUserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source="avatar.url")

    class Meta:
        model = User
        fields = ["id", "firstName", "lastName", "avatar"]
        read_only_fields = ["id", "firstName", "lastName", "avatar"]


class ChatsSerializer(serializers.ModelSerializer):
    user1 = ChatUserSerializer(read_only=True, many=False)
    user2 = ChatUserSerializer(read_only=True, many=False)

    class Meta:
        model = Chat
        fields = "__all__"
