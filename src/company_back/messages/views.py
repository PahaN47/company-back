from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from company_back.models import Message
from .serializers import MessagesSerializer


class MessagesViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = MessagesSerializer

    queryset = Message.objects.all()

    def get_queryset(self):
        query = self.queryset
        user = self.request.user
        if user.is_anonymous:
            return query.none()
        chat_id = self.kwargs.get("chat_id")
        if chat_id:
            return query.filter(chat_id=chat_id)
        return query
