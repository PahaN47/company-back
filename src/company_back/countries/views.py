from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from company_back.models import Country
from .serializers import CountrySerializer


class CountriesViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = CountrySerializer

    queryset = Country.objects.all()
