from django.contrib import admin
from django.db.models import Q

from .models import NFT, CategoryNFT, CollectionNFT, DrawNFT, SaleNFT

from django.urls import reverse
from django.shortcuts import redirect

from django.contrib.contenttypes.models import ContentType

from django_object_actions import DjangoObjectActions

from .forms import NFTCollectionForm, NFTDrawForm, NFTSaleForm, NFTForm
from .filters import (NFTCollectionIdFilter, NFTCollectionWalletFilter, NFTCollectionUsernameFilter,
                      NFTCollectionCategoryFilter, NFTCollectionFilter)


@admin.register(CategoryNFT)
class CategoryNFTAdmin(admin.ModelAdmin):
    pass


@admin.register(DrawNFT)
class DrawNFTAdmin(admin.ModelAdmin):
    form = NFTDrawForm
    exclude = ("user",)
    list_display = ("start_date", "finish_date", "category")

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        else:
            return super(DrawNFTAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        else:
            return super(DrawNFTAdmin, self).has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        else:
            return super(DrawNFTAdmin, self).has_add_permission(request)

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change or not instance.user:
            instance.user = request.user
        instance.save()
        form.save_m2m()
        return instance


@admin.register(SaleNFT)
class SaleNFTAdmin(admin.ModelAdmin):
    form = NFTSaleForm
    exclude = ("user",)
    list_display = ("start_date", "finish_date", "content_object")

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        else:
            return super(SaleNFTAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        else:
            return super(SaleNFTAdmin, self).has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        else:
            return super(SaleNFTAdmin, self).has_add_permission(request)

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change or not instance.user:
            instance.user = request.user
        instance.save()
        form.save_m2m()
        return instance

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == "content_type":
            return ContentType.objects.filter(model__in=(NFT._meta.model_name, CategoryNFT._meta.model_name))
        return super(SaleNFTAdmin, self).get_field_queryset(db, db_field, request)


@admin.register(NFT)
class NFTAdmin(DjangoObjectActions, admin.ModelAdmin):
    form = NFTForm
    exclude = ('is_mint', 'address', 'index')
    list_display = ('name', 'price', 'collection', 'address', 'is_mint')
    search_fields = ('name', 'description')
    list_filter = (NFTCollectionFilter,)
    change_actions = ('mint',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        else:
            return super(NFTAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        else:
            return super(NFTAdmin, self).has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        else:
            return super(NFTAdmin, self).has_add_permission(request)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return NFT.objects.filter(user_id=request.user.pk)
        return super(NFTAdmin, self).get_queryset(request)

    def get_form(self, request, obj=None, **kwargs):
        admin_form = super(NFTAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(admin_form):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                if obj:
                    kwargs['address'] = obj.address
                    kwargs['index'] = obj.index

                return admin_form(*args, **kwargs)

        return AdminFormWithRequest

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == "collection":
            return CollectionNFT.objects.filter(user_id=request.user.pk).exclude(Q(address=None) | Q(address=""))
        return super(NFTAdmin, self).get_field_queryset(db, db_field, request)

    def mint(self, request, obj):
        if not obj.is_mint:
            obj.is_mint = True
            obj.save()

    def get_change_actions(self, request, object_id, form_url):
        actions = super(NFTAdmin, self).get_change_actions(request, object_id, form_url)
        actions = list(actions)

        obj = self.model.objects.get(pk=object_id)
        if obj.is_mint:
            actions.remove('mint')

        return actions


@admin.register(CollectionNFT)
class NFTCollectionAdmin(DjangoObjectActions, admin.ModelAdmin):
    form = NFTCollectionForm
    list_display = ('name', 'description', 'list_categories', 'address', 'is_approved_to_sale')
    fields = ('name', 'description', 'image', 'categories')
    search_fields = ('name',)
    list_filter = (NFTCollectionIdFilter, NFTCollectionWalletFilter,
                   NFTCollectionUsernameFilter, NFTCollectionCategoryFilter)
    changelist_actions = ('create_sale', 'create_draw')
    change_actions = ("approve",)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        else:
            return super(NFTCollectionAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        else:
            return super(NFTCollectionAdmin, self).has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        else:
            return super(NFTCollectionAdmin, self).has_add_permission(request)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return CollectionNFT.objects.filter(user_id=request.user.pk)
        return super(NFTCollectionAdmin, self).get_queryset(request)

    def get_form(self, request, obj=None, **kwargs):

        admin_form = super(NFTCollectionAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(admin_form):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                if obj:
                    kwargs['address'] = obj.address

                return admin_form(*args, **kwargs)

        return AdminFormWithRequest


    def list_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])

    def create_sale(self, request, queryset):
        return redirect(reverse(f"admin:{SaleNFT._meta.app_label}_{SaleNFT._meta.model_name}_add"))

    def create_draw(self, request, queryset):
        return redirect(reverse(f"admin:{DrawNFT._meta.app_label}_{DrawNFT._meta.model_name}_add"))

    def approve(self, request, obj):
        if not obj.is_approved_to_sale:
            obj.is_approved_to_sale = True
            obj.save()

    def get_change_actions(self, request, object_id, form_url):
        actions = list(super(NFTCollectionAdmin, self).get_change_actions(request, object_id, form_url))

        obj = self.model.objects.get(pk=object_id)
        if obj.is_approved_to_sale or not request.user.is_superuser:
            actions.remove('approve')

        return actions

    def get_changelist_actions(self, request):
        actions = list(super(NFTCollectionAdmin, self).get_changelist_actions(request))

        if not request.user.collections.exists():
            actions.remove('create_sale')
            actions.remove('create_draw')

        return actions

