import sys
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from company_back.const import Role
from company_back.models import Media, User
from .serializers import ProfileSerializer


class ProfileViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = ProfileSerializer

    queryset = User.objects.exclude(role=Role.ADMIN)

    def partial_update(self, request, *args, pk=None, **kwargs):
        user = request.user
        if pk != user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        kwargs["pk"] = user.id

        avatar_url = None
        try:
            avatar_url = request.data["avatar"]
            old_avatar_url = Media.objects.get(id=user.avatar.id).url
        except Exception:
            old_avatar_url = None
        if avatar_url and avatar_url != old_avatar_url:
            new_avatar = Media.objects.create(url=avatar_url)
            new_avatar.save()
            request.data["avatar"] = new_avatar.id
        return super().partial_update(request, *args, **kwargs)
