from django.conf import settings
import jwt
from rest_framework import authentication, exceptions

from company_back.const import AUTH_TOKEN_NAME
from company_back.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        request.user = None
        token = request.COOKIES.get(AUTH_TOKEN_NAME)

        if token is None:
            return None

        if len(token) > 255:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception as exc:
            raise exceptions.AuthenticationFailed(
                "Ошибка аутентификации. Невозможно декодировать токен."
            ) from exc

        try:
            user = User.objects.get(id=payload["id"])
        except Exception as exc:
            raise exceptions.AuthenticationFailed("Данный пользователь деактивирован.") from exc

        return (user, token)
