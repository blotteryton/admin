from django.contrib import admin

from administration.models import MarketplaceConfiguration
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("header", "description", "category")
    list_filter = ("category",)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            if (not request.user.has_wallet or not request.user.is_wallet_deployed
                    or not MarketplaceConfiguration.get_solo().marketplace_deployed):
                return False
        return super(NotificationAdmin, self).has_module_permission(request)
