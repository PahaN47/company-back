from rest_framework import serializers

from company_back.models import Chat


class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
