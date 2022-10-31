from django.apps import AppConfig

from .utils import table_exists


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = "My NFT"

    def ready(self):
        if not table_exists("auth_group"):
            return

        from .models import NFT, CollectionNFT
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        bloggers, created = Group.objects.get_or_create(name='bloggers')
        if created:
            bloggers.permissions.add(
                *Permission.objects.filter(content_type__in=(ContentType.objects.get_for_model(NFT).id,
                                                             ContentType.objects.get_for_model(CollectionNFT).id)),
            )
