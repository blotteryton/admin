from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class GetTokenParamsSerializer(serializers.Serializer):
    user_uid = serializers.CharField()

    class Meta:
        fields = ("user_uid",)


class GetTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        fields = ("token",)
