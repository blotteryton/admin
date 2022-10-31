from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import NFT, CollectionNFT

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


class NFTAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    list_filter = (('user__collections', admin.RelatedOnlyFieldListFilter),)

    def get_queryset(self, request):
        return NFT.objects.filter(user_id=request.user.pk)

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == "collection":
            return CollectionNFT.objects.filter(user_id=request.user.pk)
        return super(NFTAdmin, self).get_field_queryset(db, db_field, request)

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change or not instance.user:
            instance.user = request.user
        instance.save()
        form.save_m2m()
        return instance


class NFTCollectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def get_queryset(self, request):
        return CollectionNFT.objects.filter(user_id=request.user.pk)

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change or not instance.user:
            instance.user = request.user
        instance.save()
        form.save_m2m()
        return instance


admin.site.register(CollectionNFT, NFTCollectionAdmin)
admin.site.register(NFT, NFTAdmin)
