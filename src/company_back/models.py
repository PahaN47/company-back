from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from company_back.const import MatchStatus, MessageStatus, PurchaseStatus, Role
from .managers import CustomUserManager


# Create your models here.
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
    role = models.CharField(max_length=16, default=Role.USER, blank=True, null=False)
    balance = models.OneToOneField(
        Balance, on_delete=models.DO_NOTHING, default=None, blank=True, null=True
    )
    avatar = models.OneToOneField(
        Media, on_delete=models.DO_NOTHING, default=None, blank=True, null=True
    )
    gender = models.CharField(max_length=32, default=None, blank=True, null=True)
    birthDate = models.DateField()
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, default=None, blank=True, null=True
    )
    timezone = models.IntegerField(default=None, blank=True, null=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["firstName", "birthDate", "password"]

    objects = CustomUserManager()

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

    def __str__(self):
        return str(self.email)


class Purchase(models.Model):
    balance = models.ForeignKey(Balance, on_delete=models.DO_NOTHING)
    gift = models.ForeignKey(Gift, on_delete=models.DO_NOTHING)
    reciever = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=16, default=PurchaseStatus.PENDING, blank=True, null=False)
    date = models.DateField(default=None, blank=True, null=True)


class Match(models.Model):
    status = models.CharField(max_length=16, default=MatchStatus.PENDING, blank=True, null=False)
    initiator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="initiator")
    reciever = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reciever")
    date = models.DateField(default=None, blank=True, null=True)


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user2")


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=256)
    date = models.DateTimeField()
    status = models.CharField(max_length=16, default=MessageStatus.SENT, blank=True, null=False)
    gift = models.ForeignKey(Gift, on_delete=models.DO_NOTHING)
