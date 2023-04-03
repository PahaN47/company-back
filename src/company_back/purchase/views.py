from rest_framework import status

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from company_back.models import Purchase
from .serializers import PurchaseSerializer


class PurchseViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = PurchaseSerializer

    queryset = Purchase.objects.all()

    @action(methods=["post"], detail=False)
    def make_purchase(self, request):
        user = request.user
        balance_id = user.balance.id
        data = dict(request.data)
        data["balance"] = balance_id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
