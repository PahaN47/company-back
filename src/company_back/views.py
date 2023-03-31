from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from company_back.const import AUTH_TOKEN_NAME
from company_back.serializers import RegisterSerializer, LoginSerializer


class RegisterAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.set_cookie(key=AUTH_TOKEN_NAME, value=serializer.data.get("token"))

        return response


class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.set_cookie(key=AUTH_TOKEN_NAME, value=serializer.data.get("token"))

        return response


class LogoutAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.user

        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(AUTH_TOKEN_NAME)

        return response
