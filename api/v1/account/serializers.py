from django.contrib.auth import get_user_model

from rest_framework import serializers

from api.v1.account.utils import convert_ton_rub, convert_ton_usd

User = get_user_model()


class GetTokenParamsSerializer(serializers.Serializer):
    user_uid = serializers.CharField()

    class Meta:
        model = User
        fields = ("user_uid",)


class BalanceSerializer(serializers.ModelSerializer):
    ton = serializers.SerializerMethodField()
    rub = serializers.SerializerMethodField()
    usd = serializers.SerializerMethodField()

    def get_ton(self, obj):
        return obj.wallet_balance

    def get_rub(self, obj):
        return convert_ton_rub(obj.wallet_balance)

    def get_usd(self, obj):
        return convert_ton_usd(obj.wallet_balance)

    class Meta:
        model = User
        fields = ("ton", "rub", "usd")


class UserMeSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        return BalanceSerializer(instance=obj).data

    class Meta:
        model = User
        fields = ("wallet_address", "balance", "is_wallet_deployed")


class TransferSerializer(serializers.Serializer):
    destWallet = serializers.CharField()
    amount = serializers.CharField()

    class Meta:
        fields = ("destWallet", "amount")
