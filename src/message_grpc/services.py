from django_socio_grpc import generics
from company_back.models import Message
from .serializers import MessageProtoSerializer


class MessageService(generics.AsyncModelService):
    queryset = Message.objects.all()
    serializer_class = MessageProtoSerializer
