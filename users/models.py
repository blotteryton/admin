from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType

from users.utils import get_wallet_balance


class User(AbstractUser):
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    wallet_public_key = models.CharField(max_length=255, blank=True, null=True)
    wallet_secret_key = models.CharField(max_length=255, blank=True, null=True)
    wallet_mnemonic = models.CharField(max_length=255, blank=True, null=True)

    def has_perm(self, perm, obj=None):
        codename = perm.split(".")[-1]
        nft_ct = ContentType.objects.get_for_model(NFT)
        collection_nft_ct = ContentType.objects.get_for_model(CollectionNFT)

        if (nft_ct.permission_set.filter(codename=codename).exists() or
           collection_nft_ct.permission_set.filter(codename=codename).exists()) and not self.has_wallet:
            return False

        if nft_ct.permission_set.filter(codename=codename).exists() and not self.collections.exists():
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "NFT"
        verbose_name_plural = "NFT"


class CollectionNFT(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, editable=False, related_name="collections")
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "NFT collection"
        verbose_name_plural = "NFT collections"
