from django.forms import model_to_dict
from rest_framework import status

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from company_back.models import Balance
from .serializers import BalanceSerializer


class BalanceViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = BalanceSerializer

    queryset = Balance.objects.all()

    @action(methods=["get"], detail=False)
    def get_own(self, request):
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        balance_id = user.balance_id
        if user.balance_id is None:
            new_balance = Balance.objects.create(amount=0)
            serializer = self.serializer_class(data=model_to_dict(new_balance))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            balance_id = serializer.data["id"]
            setattr(user, "balance_id", balance_id)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        balance = Balance.objects.get(id=balance_id)
        serializer = self.serializer_class(data=model_to_dict(balance))
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False)
    def add_to_balance(self, request):
        balance = request.user.balance
        amount = request.data.get("amount")
        setattr(balance, "amount", balance.amount + amount)
        balance.save()
        return Response(model_to_dict(balance), status=status.HTTP_201_CREATED)
