from django.apps import apps
from django.core.cache import cache
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType

from administration.models import MarketplaceConfiguration, Configuration
from nft.utils import create_marketplace, deploy_marketplace
from users.utils import get_wallet_balance, get_wallet_deployed, deploy_wallet, create_wallet


class User(AbstractUser):
    telegram_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    wallet_public_key = models.CharField(max_length=255, blank=True, null=True)
    wallet_secret_key = models.CharField(max_length=255, blank=True, null=True)
    wallet_mnemonic = models.CharField(max_length=255, blank=True, null=True)
    wallet_deployed = models.BooleanField(default=False)

    avatar = models.ImageField(upload_to="blogger_avatars/", blank=True, null=True)
    cover = models.ImageField(upload_to="blogger_covers/", blank=True, null=True)

    def has_perm(self, perm, obj=None):
        if not self.is_superuser:
            codename = perm.split(".")[-1]
            group = self.groups.get(name="bloggers")

            if group.permissions.filter(codename=codename).exists() and (
                    not self.has_wallet or not self.is_wallet_deployed
                    or not MarketplaceConfiguration.get_solo().marketplace_deployed
                    or not Configuration.get_solo().is_configured()
            ):
                return False

            if group.permissions.filter(
                    content_type__in=ContentType.objects.get_for_models(
                        apps.get_model("nft.NFT"), apps.get_model("nft.DrawNFT"), apps.get_model("nft.SaleNFT")
                    ).values(),
                    codename=codename
            ).exists() and not self.collections.exists():
                return False

        return super(User, self).has_perm(perm, obj)

    @property
    def has_wallet(self):
        return self.wallet_address and self.wallet_public_key and self.wallet_secret_key and self.wallet_mnemonic

    @property
    def wallet_balance(self):
        balance = get_wallet_balance(address=self.wallet_address)
        if float(balance) > 0.05 and not self.wallet_deployed and not cache.get(f"send_deploy_{self.wallet_address}"):
            deploy_wallet(self)

        if self.is_superuser:
            from administration.models import MarketplaceConfiguration

            market_conf = MarketplaceConfiguration.get_solo()
            if not market_conf.marketplace_address:
                if address := create_marketplace(self).get("address"):
                    market_conf.marketplace_address = address
                    market_conf.save()
            else:
                if float(balance) > 0.5 and not market_conf.marketplace_deployed:
                    response = deploy_marketplace(self, market_conf.marketplace_address)
                    if response.get("@type") == "ok":
                        market_conf.marketplace_deployed = True
                        market_conf.save()

        return balance

    @property
    def is_wallet_deployed(self):
        if not self.wallet_deployed:
            is_deployed = get_wallet_deployed(self.wallet_address)
            if self.wallet_deployed != is_deployed:
                self.wallet_deployed = is_deployed
                self.save()
            return is_deployed

        return self.wallet_deployed
