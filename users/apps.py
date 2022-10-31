from django.apps import AppConfig
from .utils import table_exists


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = "My NFT"

    def ready(self):
        if not table_exists("auth_group"):
            return

        from django.contrib.auth.models import Group

        Group.objects.get_or_create(name='bloggers')
