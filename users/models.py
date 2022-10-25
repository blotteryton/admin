from django.db import models
from django.contrib.auth.models import AbstractUser

#variable for getting user id
exposed_request = ""

class User(AbstractUser):
    ton_adress = models.CharField(max_length=255)

def get_user_id():
    print(exposed_request.user.id)
    return exposed_request.user.id

class NFT(models.Model):
  collection = models.ForeignKey('CategoryNFT', on_delete=models.PROTECT)
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  price = models.CharField(max_length=255)
  image = models.ImageField(upload_to="photos/%Y/%m/%d/")
  user_id = models.IntegerField(User, default=get_user_id, editable=False)

  class Meta:
      verbose_name = "NFT"
      verbose_name_plural = "NFT"

class CategoryNFT(models.Model):
  name = models.CharField(max_length=255, db_index=True)
  user_id = models.IntegerField(User, default=get_user_id, editable=False)

  class Meta:
      verbose_name = "NFT categories"
      verbose_name_plural = "NFT categories"
