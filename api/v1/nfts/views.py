from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from nft.models import NFT
from api.v1.nfts.serializers import NFTSerializer


User = get_user_model()


class NftView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = NFTSerializer
    queryset = NFT.objects.filter(collection__is_approved_to_sale=True)
