import coreapi
import coreschema
from django.forms import model_to_dict

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import BaseFilterBackend

from company_back.const import Role
from company_back.models import User, Match
from .serializers import UsersSerializer


class UsersPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 6


class UsersFilterListBackend(BaseFilterBackend):
    def get_schema_fields(self, _):
        return [
            coreapi.Field(
                name="gender",
                location="query",
                required=False,
                schema=coreschema.String(description="gender"),
            ),
            coreapi.Field(
                name="country",
                location="query",
                required=False,
                schema=coreschema.Integer(description="country id"),
            ),
            coreapi.Field(
                name="min_age",
                location="query",
                required=False,
                schema=coreschema.Integer(description="min age"),
            ),
            coreapi.Field(
                name="max_age",
                location="query",
                required=False,
                schema=coreschema.Integer(description="max age"),
            ),
        ]

    def filter_queryset(self, request, queryset, _):
        gender = request.query_params.get("gender")
        country_id = request.query_params.get("country")
        min_age = request.query_params.get("min_age")
        max_age = request.query_params.get("max_age")

        query = queryset
        try:
            if gender:
                query = query.filter(gender=gender)
            if country_id:
                query = query.filter(country_id=country_id)
            if min_age:
                query = query.filter(age__gte=min_age)
            if max_age:
                query = query.filter(age__lte=max_age)
            return query
        except Exception:
            return queryset.none()


class UsersViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = UsersSerializer

    pagination_class = UsersPagination
    filter_backends = [UsersFilterListBackend]

    queryset = User.objects.exclude(role=Role.ADMIN.value)

    def get_queryset(self):
        user = self.request.user

        gender = self.request.query_params.get("gender")
        country_id = self.request.query_params.get("country")
        min_age = self.request.query_params.get("min_age")
        max_age = self.request.query_params.get("max_age")

        matches_recieved = [id[0] for id in list(Match.objects.filter(reciever=user.id).values_list("initiator"))]
        matches_initiated = [id[0] for id in list(Match.objects.filter(initiator=user.id).values_list("reciever"))]
        exclude_list = matches_recieved + matches_initiated + [user.id]

        query = self.queryset.exclude(id__in=exclude_list)
        try:
            if gender:
                query = query.filter(gender=gender)
            if country_id:
                query = query.filter(country_id=country_id)
            if min_age:
                query = query.filter(age__gte=min_age)
            if max_age:
                query = query.filter(age__lte=max_age)
            return query
        except Exception:
            return self.queryset.none()
