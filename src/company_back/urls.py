from django.contrib import admin
from django.urls import path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from company_back.auth.views import LoginAPIView, RegisterAPIView, LogoutAPIView
from company_back.balance.views import BalanceViewSet
from company_back.chats.views import ChatsViewSet
from company_back.countries.views import CountriesViewSet
from company_back.gifts.views import GiftsViewSet
from company_back.matches.views import CreateMatchAPIView, MatchesViewSet
from company_back.messages.views import MessagesViewSet
from company_back.profile.views import ProfileViewSet
from company_back.purchase.views import PurchseViewSet
from company_back.users.views import UsersViewSet

auth_register = RegisterAPIView.as_view()
auth_login = LoginAPIView.as_view()
auth_logout = LogoutAPIView.as_view()

profile = ProfileViewSet.as_view({"get": "retrieve", "patch": "partial_update"})

users = UsersViewSet.as_view({"get": "list"})

matches_outgoing = MatchesViewSet.as_view({"get": "get_outgoing"})
matches_incoming = MatchesViewSet.as_view({"get": "get_incoming"})
matches_accept = MatchesViewSet.as_view({"post": "accept"})
matches_reject = MatchesViewSet.as_view({"post": "reject"})
mathces_create = CreateMatchAPIView.as_view()

chats = ChatsViewSet.as_view({"get": "list"})

messages_get = MessagesViewSet.as_view({"get": "list"})
messages_delete = MessagesViewSet.as_view({"delete": "destroy"})

countries = CountriesViewSet.as_view({"get": "list"})

gifts_get_list = GiftsViewSet.as_view({"get": "list"})
gifts_get = GiftsViewSet.as_view({"get": "retrieve"})

balance_get = BalanceViewSet.as_view({"get": "get_own"})
balance_add = BalanceViewSet.as_view({"post": "add_to_balance"})

purchase = PurchseViewSet.as_view({"post": "make_purchase"})


schema_view = get_schema_view(
    openapi.Info(
        title="Company API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("swagger/swagger.json/", schema_view.without_ui(), name="schema-swagger-ui-json"),
    path("auth/register", auth_register),
    path("auth/login", auth_login),
    path("auth/logout", auth_logout),
    path("profile/<int:pk>", profile),
    path("users", users),
    path("matches/", mathces_create),
    path("matches/outgoing", matches_outgoing),
    path("matches/incoming", matches_incoming),
    path("matches/accept/<int:pk>", matches_accept),
    path("matches/reject/<int:pk>", matches_reject),
    path("chats/", chats),
    path("messages/<int:chat_id>", messages_get),
    path("messages/delete/<int:pk>", messages_delete),
    path("countries/", countries),
    path("gifts/", gifts_get_list),
    path("gifts/<int:pk>", gifts_get),
    path("balance/", balance_get),
    path("balance/add/", balance_add),
    path("purchase/", purchase),
]
