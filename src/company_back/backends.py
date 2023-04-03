import jwt

from django.conf import settings

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
                "Authentication failed. Can not decode token"
            ) from exc

        try:
            user = User.objects.get(id=payload["id"])
        except Exception as exc:
            raise exceptions.AuthenticationFailed("This user does not exist") from exc

        return (user, token)
