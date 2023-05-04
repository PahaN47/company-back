from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from company_back.const import Role
from company_back.models import User
from .serializers import ProfileSerializer


class ProfileViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = ProfileSerializer

    queryset = User.objects.exclude(role=Role.ADMIN)

    def partial_update(self, request, *args, pk=None, **kwargs):
        user_id = request.user.id
        if pk != user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        kwargs["pk"] = user_id
        return super().partial_update(request, *args, **kwargs)
