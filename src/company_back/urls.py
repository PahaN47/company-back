from rest_framework import permissions
from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from company_back.views import LoginAPIView, RegisterAPIView, LogoutAPIView

auth_register = RegisterAPIView.as_view()
auth_login = LoginAPIView.as_view()
auth_logout = LogoutAPIView.as_view()


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
    path("auth/register", auth_register),
    path("auth/login", auth_login),
    path("auth/logout", auth_logout),
]
