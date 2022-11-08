from django.contrib import admin
from django.contrib.auth import get_user_model
from solo.admin import SingletonModelAdmin

from nft.models import CollectionNFT
from .models import Project, ProjectMember, Configuration, MarketplaceConfiguration


User = get_user_model()


class ProjectMemberInline(admin.StackedInline):
    model = ProjectMember
    exclude = ("user",)
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectMemberInline, ]


@admin.register(Configuration)
class ConfigurationAdmin(SingletonModelAdmin):
    pass


@admin.register(MarketplaceConfiguration)
class MarketplaceConfigurationAdmin(SingletonModelAdmin):
    def get_field_queryset(self, db, db_field, request):
        if db_field.name in ("recommended_collections", "popular_collections"):
            return CollectionNFT.objects.filter(is_approved_to_sale=True).exclude(user__projectmember=None)

        if db_field.name == "recommended_authors":
            return User.objects.filter(is_superuser=False, is_staff=True).exclude(projectmember=None)

        return super(MarketplaceConfigurationAdmin, self).get_field_queryset(db, db_field, request)
