from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from users.utils import get_wallet_balance


class User(AbstractUser):
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    wallet_public_key = models.CharField(max_length=255, blank=True, null=True)
    wallet_secret_key = models.CharField(max_length=255, blank=True, null=True)
    wallet_mnemonic = models.CharField(max_length=255, blank=True, null=True)

    def has_perm(self, perm, obj=None):
        if not self.is_superuser:
            codename = perm.split(".")[-1]

            group = self.groups.get(name="bloggers")

            if group.permissions.filter(codename=codename).exists() and not self.has_wallet:
                return False

            if (group.permissions.filter(
                    content_type=ContentType.objects.get_for_model(NFT), codename=codename
            ).exists() or group.permissions.filter(
                    content_type=ContentType.objects.get_for_model(DrawNFT), codename=codename
            ).exists() or group.permissions.filter(
                    content_type=ContentType.objects.get_for_model(SaleNFT), codename=codename
            ).exists()) and not self.collections.exists():
                return False

        return super(User, self).has_perm(perm, obj)

    @property
    def has_wallet(self):
        return self.wallet_address and self.wallet_public_key and self.wallet_secret_key and self.wallet_mnemonic

    def wallet_balance(self):
        return get_wallet_balance(address=self.wallet_address)


class NFT(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, editable=False)
    collection = models.ForeignKey('CollectionNFT', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=255)
    image = models.ImageField(upload_to="photos/%Y/%m/%d/")

    is_mint = models.BooleanField(default=False)

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
    category = models.ForeignKey(to=CategoryNFT, on_delete=models.PROTECT, blank=True, null=True)

    is_approved_to_sale = models.BooleanField(default=False)

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
