from django.db.models import Sum, Min
from django.contrib.auth import get_user_model

from rest_framework import serializers

from nft.models import CollectionNFT, NFT


User = get_user_model()


class NFTCollectionSerializer(serializers.ModelSerializer):
    floor_price = serializers.SerializerMethodField()

    def get_floor_price(self, obj: CollectionNFT):
        return obj.nft_set.filter(collection__is_approved_to_sale=True).aggregate(Min("price")).get("price__min")

    class Meta:
        model = CollectionNFT
        fields = ("id", "image", "name", "floor_price")


class CollectionNFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = ("id", "name", "image", "price")


class CollectionNFTInfoSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    total_cash = serializers.SerializerMethodField()
    floor_price = serializers.SerializerMethodField()

    def get_creator(self, obj):
        return obj.user.projectmember_set.first().project.name

    def get_items(self, obj):
        return obj.nft_set.count()

    def get_total_cash(self, obj):
        total = obj.nft_set.aggregate(Sum("price")).get("price__sum")
        return round(total / 1000, 4) if total else 0

    def get_floor_price(self, obj):
        minimal = obj.nft_set.aggregate(Min("price")).get("price__min")
        return minimal if minimal else 0

    class Meta:
        model = CollectionNFT
        fields = ("creator", "items", "total_cash", "floor_price")


class CollectionAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "avatar", "cover", "first_name", "last_name")


class NFTCollectionRetrieveSerializer(serializers.ModelSerializer):
    author = CollectionAuthorSerializer(source="user")
    info = serializers.SerializerMethodField()

    def get_info(self, obj):
        return CollectionNFTInfoSerializer(instance=obj).data

    class Meta:
        model = CollectionNFT
        fields = ("id", "author", "info",)
