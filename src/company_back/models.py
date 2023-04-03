import jwt

from datetime import datetime as dt, timedelta

from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from company_back.const import MatchStatus, MessageStatus, PurchaseStatus, Role
from company_back.managers import CustomUserManager


class Country(models.Model):
    name = models.CharField(max_length=128)


class Balance(models.Model):
    amount = models.IntegerField(default=0, blank=True, null=False)


class Media(models.Model):
    url = models.CharField(max_length=1024)


class Gift(models.Model):
    image = models.OneToOneField(Media, on_delete=models.CASCADE)
    price = models.IntegerField(default=0, blank=True, null=False)


class User(AbstractBaseUser):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64, default=None, blank=True, null=True)
    phone = models.CharField(max_length=32, default=None, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=16, default=Role.USER.value, blank=True, null=False)
    balance = models.OneToOneField(
        Balance, on_delete=models.SET_NULL, default=None, blank=True, null=True
    )
    avatar = models.OneToOneField(
        Media, on_delete=models.SET_NULL, default=None, blank=True, null=True
    )
    gender = models.CharField(max_length=32, default=None, blank=True, null=True)
    birthDate = models.DateField()
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, default=None, blank=True, null=True
    )
    timezone = models.IntegerField(default=None, blank=True, null=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["firstName", "birthDate", "password"]

    objects = CustomUserManager()

    @property
    def age(self):
        return relativedelta(dt.now(), self.birthDate).years

    @property
    def is_staff(self):
        return self.role == Role.ADMIN

    @property
    def is_superuser(self):
        return self.role == Role.ADMIN

    @property
    def has_module_perms(self):
        return lambda x: self.role == Role.ADMIN

    @property
    def has_perm(self):
        return lambda x: self.role == Role.ADMIN

    @property
    def token(self):
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        exp_date = dt.now() + timedelta(days=1)

        token = jwt.encode(
            {"id": self.pk, "exp": int(exp_date.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    def __str__(self):
        return str(self.email)


class Purchase(models.Model):
    balance = models.ForeignKey(
        Balance, on_delete=models.SET_NULL, default=None, blank=True, null=True
    )
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=16, default=PurchaseStatus.PENDING.value, blank=True, null=False
    )
    date = models.DateField(blank=True, null=True, auto_now=True)


class Match(models.Model):
    status = models.CharField(
        max_length=16, default=MatchStatus.PENDING.value, blank=True, null=False
    )
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initiator")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciever")
    date = models.DateField(blank=True, null=True, auto_now=True)


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=256)
    date = models.DateTimeField(blank=True, null=True, auto_now=True)
    status = models.CharField(
        max_length=16, default=MessageStatus.SENT.value, blank=True, null=False
    )
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, default=None, blank=True, null=True)
