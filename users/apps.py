from django.db.models import Q
from django.apps import AppConfig

from .utils import table_exists


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = "My NFT"

    def ready(self):
        if not table_exists("auth_group"):
            return

        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import NFT, CollectionNFT, CategoryNFT, DrawNFT, SaleNFT

        bloggers, created = Group.objects.get_or_create(name='bloggers')
        bloggers.permissions.add(
            *Permission.objects.filter(content_type__in=(ContentType.objects.get_for_model(NFT).id,
                                                         ContentType.objects.get_for_model(CollectionNFT).id)),
            *Permission.objects.filter(Q(codename__startswith="add") | Q(codename__startswith="view"),
                                       content_type__in=(ContentType.objects.get_for_model(CategoryNFT).id,
                                                         ContentType.objects.get_for_model(DrawNFT).id,
                                                         ContentType.objects.get_for_model(SaleNFT).id)),
        )
