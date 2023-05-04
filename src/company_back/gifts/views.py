from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from company_back.models import Gift
from .serializers import GiftsSerializer


class GiftsViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = GiftsSerializer

    queryset = Gift.objects.all()
