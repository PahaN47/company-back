from django.db import models

# Create your models here.
class country(models.Model):
    name = models.CharField(max_length=128)

class balance(models.Model):
    amount = models.IntegerField(default=0,blank=True, null=True)

class media(models.Model):
    urt = models.CharField(max_length=1024)

class gift(models.Model):
    imageId = models.OneToOneField(media,on_delete=models.DO_NOTHING)
    price = models.IntegerField(default=0,blank=True, null=False)


class user(models.Model):
    firstNmae = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    role = models.CharField(max_length=16)
    balanceId = models.OneToOneField(balance, on_delete=models.DO_NOTHING)
    avatarId = models.OneToOneField(media, on_delete=models.DO_NOTHING)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=32)
    birthDate = models.DateField()
    country = models.ForeignKey(country, on_delete=models.DO_NOTHING)
    timezone = models.IntegerField(default=0,blank=True, null=False)

class purchase(models.Model):
    balanceId = models.ForeignKey(balance, on_delete=models.DO_NOTHING)
    giftid = models.ForeignKey(gift, on_delete=models.DO_NOTHING)
    reciverId = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=16)
    date = models.DateTimeField()

class match(models.Model):
    status = models.CharField(max_length=16)
    initiatorId = models.ForeignKey(user, on_delete=models.DO_NOTHING,related_name ="initiator")
    reciverId = models.ForeignKey(user, on_delete=models.DO_NOTHING,related_name="reciver")
    date = models.DateTimeField()

class chat(models.Model):
    user1Id = models.ForeignKey(user, on_delete=models.DO_NOTHING,related_name = 'user1')
    user2Id = models.ForeignKey(user, on_delete=models.DO_NOTHING,related_name ="user2")

class message(models.Model):
    chatId = models.ForeignKey(chat, on_delete=models.DO_NOTHING)
    userId = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=256)
    date = models.DateTimeField()
    status = models.CharField(max_length=16)
    giftId = models.ForeignKey(gift, on_delete=models.DO_NOTHING)




