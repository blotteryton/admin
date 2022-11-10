from rest_framework import serializers

from django.contrib.auth import get_user_model

from nft.models import NFT, CategoryNFT


User = get_user_model()


class CollectionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNFT
        fields = ("id", "name",)


class NFTSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_categories(self, obj):
        return CollectionCategorySerializer(instance=obj.collection.categories.all(), many=True).data

    class Meta:
        model = NFT
        fields = ("id", "username", "name", "description", "image", "price", "categories", "sale_address")
