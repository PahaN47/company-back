from django_socio_grpc.utils.servicer_register import AppHandlerRegistry
from .services import MessageService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry("message_grpc", server)
    app_registry.register(MessageService)
