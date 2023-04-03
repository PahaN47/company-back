from django.db.models import Q

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from company_back.models import Chat
from .serializers import ChatsSerializer


class ChatsViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = ChatsSerializer

    queryset = Chat.objects.all()

    def get_queryset(self):
        query = self.queryset
        user = self.request.user
        if user.is_anonymous:
            return query.none()
        return query.filter(Q(user1_id=user.id) | Q(user2_id=user.id))
