from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.datetime_safe import date

from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, ListAPIView

from administration.models import MarketplaceConfiguration
from nft.models import CollectionNFT

from api.v1.collections.serializers import (NFTCollectionRetrieveSerializer, NFTCollectionSerializer,
                                            CollectionNFTSerializer)


User = get_user_model()


class CollectionView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = NFTCollectionRetrieveSerializer
    queryset = CollectionNFT.objects.filter(is_approved_to_sale=True)


class CollectionsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = NFTCollectionSerializer
    queryset = CollectionNFT.objects.filter(is_approved_to_sale=True)


class CollectionNftsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CollectionNFTSerializer

    def get_queryset(self):
        collection_id = self.kwargs.get("pk")
        collection = CollectionNFT.objects.filter(id=collection_id, is_approved_to_sale=True)

        return collection.first().nft_set.all() if collection else collection


class CollectionNewView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = NFTCollectionSerializer
    queryset = CollectionNFT.objects.filter(created_at__gt=date.today() - timedelta(days=7),
                                            is_approved_to_sale=True).order_by("-created_at")


class CollectionPopularView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = NFTCollectionSerializer

    def get_queryset(self):
        return MarketplaceConfiguration.get_solo().popular_collections.get_queryset().order_by("id")
