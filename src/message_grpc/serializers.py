from django_socio_grpc import proto_serializers
from .grpc import message_grpc_pb2 as message_pb2
from company_back.models import Message


class MessageProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Message
        proto_class = message_pb2.MessageResponse
        proto_class_list = message_pb2.MessageListResponse
        fields = ["id", "chat", "user", "message", "date"]
