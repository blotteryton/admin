from django.db.models import Q
from django.db import connections

from django.apps import AppConfig


def table_exists(table_name: str, connection_name: str = "default") -> bool:
    return table_name in connections[connection_name].introspection.table_names()


class NftConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nft'
    verbose_name = "My NFT"

    def ready(self):
        if not table_exists("auth_group"):
            return

        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import NFT, CollectionNFT, CategoryNFT, DrawNFT, SaleNFT

        bloggers, created = Group.objects.get_or_create(name='bloggers')
        bloggers.permissions.clear()
        bloggers.permissions.add(
            *Permission.objects.filter(
                Q(codename__startswith="add") | Q(codename__startswith="view"),
                content_type__in=ContentType.objects.get_for_models(
                    NFT, CollectionNFT, CategoryNFT, DrawNFT, SaleNFT
                ).values()
            ),
        )
