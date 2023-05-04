from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from company_back.const import MatchStatus
from company_back.models import Match
from .serializers import CreateMatchSerializer, MatchesSerializer


class MatchesViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = MatchesSerializer

    queryset = Match.objects.exclude(status=MatchStatus.REJECTED)

    filter_incoming = False

    def get_queryset(self):
        query = self.queryset
        user = self.request.user
        if user.is_anonymous:
            return query.none()
        if self.filter_incoming:
            query = query.filter(reciever_id=user.id)
        else:
            query = query.filter(initiator_id=user.id)
        return query

    @action(methods=["get"], detail=False)
    def get_outgoing(self, request, *args, **kwargs):
        self.filter_incoming = False
        return super().list(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def get_incoming(self, request, *args, **kwargs):
        self.filter_incoming = True
        return super().list(request, *args, **kwargs)

    @action(methods=["post"], detail=False)
    def accept(self, request, *args, **kwargs):
        self.filter_incoming = True
        request.data["status"] = MatchStatus.ACCEPTED.value
        return super().partial_update(request, *args, **kwargs)

    @action(methods=["post"], detail=False)
    def reject(self, request, *args, **kwargs):
        self.filter_incoming = True
        request.data["status"] = MatchStatus.REJECTED.value
        return super().partial_update(request, *args, **kwargs)


class CreateMatchAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = CreateMatchSerializer

    def post(self, request):
        user = request.user
        if user.is_anonymous or user.id != request.data["initiator"]:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
