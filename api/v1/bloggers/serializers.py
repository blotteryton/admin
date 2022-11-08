from django.db.models import Sum, Min
from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class BloggerInfoSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total_cash = serializers.SerializerMethodField()
    floor_price = serializers.SerializerMethodField()

    def get_items(self, obj):
        return obj.nft_set.filter(collection__is_approved_to_sale=True).count()

    def get_total_cash(self, obj):
        total = obj.nft_set.filter(collection__is_approved_to_sale=True).aggregate(Sum("price")).get("price__sum")
        return round(total / 1000, 4) if total else 0

    def get_floor_price(self, obj):
        minimal = obj.nft_set.filter(collection__is_approved_to_sale=True).aggregate(Min("price")).get("price__min")
        return minimal if minimal else 0

    class Meta:
        model = User
        fields = ("items", "total_cash", "floor_price")


class BloggerSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField()

    def get_info(self, obj):
        return BloggerInfoSerializer(instance=obj).data

    class Meta:
        model = User
        fields = ("id", "avatar", "cover", "first_name", "last_name", "info")
