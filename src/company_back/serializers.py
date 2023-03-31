from rest_framework import serializers

from company_back.models import User
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "firstName",
            "email",
            "password",
            "birthDate",
            "token",
        ]

        read_only_fields = ("token",)
        extra_kwargs = {"password": {"write_only": True}, "birthDate": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "firstName", "token"]

        read_only_fields = ("firstName", "token")
        extra_kwargs = {"password": {"write_only": True}, "email": {"validators": [EmailValidator]}}

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("A user with this email and password was not found.")

        return {
            "firstName": user.firstName,
            "email": user.email,
            "password": user.password,
            "token": user.token,
        }
