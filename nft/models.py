from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class NFT(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, editable=False)
    collection = models.ForeignKey('CollectionNFT', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    image = models.ImageField(upload_to="photos/%Y/%m/%d/")

    is_mint = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    index = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "NFT"
        verbose_name_plural = "NFT"


class CategoryNFT(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "NFT category"
        verbose_name_plural = "NFT categories"


class CollectionNFT(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, editable=False, related_name="collections")
    name = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    categories = models.ManyToManyField(to=CategoryNFT, blank=True)
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)

    is_approved_to_sale = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "NFT collection"
        verbose_name_plural = "NFT collections"


class DrawNFT(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    category = models.ForeignKey(CategoryNFT, on_delete=models.PROTECT)

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name = "NFT draw"
        verbose_name_plural = "NFT draws"


class SaleNFT(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content_object.name

    class Meta:
        verbose_name = "NFT sale"
        verbose_name_plural = "NFT sales"
