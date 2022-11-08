from rest_framework import serializers

from django.contrib.auth import get_user_model

from administration.models import MarketplaceConfiguration
from api.v1.collections.serializers import NFTCollectionSerializer, CollectionAuthorSerializer
from nft.models import CollectionNFT

User = get_user_model()


class RecommendedCollectionsSerializer(serializers.ModelSerializer):
    author = CollectionAuthorSerializer(source="user")

    class Meta:
        model = CollectionNFT
        fields = ("id", "description", "author")


class RecommendedAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "avatar", "first_name", "last_name")


class RecommendationsSerializer(serializers.ModelSerializer):
    recommended_collections = RecommendedCollectionsSerializer(many=True)
    recommended_authors = RecommendedAuthorsSerializer(many=True)
    popular_collections = NFTCollectionSerializer(many=True)

    class Meta:
        model = MarketplaceConfiguration
        fields = ("recommended_collections", "popular_collections", "recommended_authors")
