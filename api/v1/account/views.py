from rest_framework import status
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from api.v1.account.utils import create_transfer
from api.v1.account.serializers import UserMeSerializer, TransferSerializer


User = get_user_model()


class MeView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMeSerializer
    queryset = User.objects.all()

    def get_object(self):

        return self.request.user


class TransferView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        create_transfer(source_wallet=user.wallet_address,
                        mnemonic=user.wallet_mnemonic,
                        dest_wallet=serializer.validated_data.get("destWallet"),
                        amount=serializer.validated_data.get("amount"))

        return Response(status=status.HTTP_202_ACCEPTED)

