from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, ListAPIView

from api.v1.bloggers.serializers import BloggerSerializer
from api.v1.collections.serializers import NFTCollectionSerializer

from nft.models import CollectionNFT


User = get_user_model()


class BloggerView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BloggerSerializer
    queryset = User.objects.filter(is_staff=True, is_superuser=False).exclude(projectmember=None)


class BloggerCollectionsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = NFTCollectionSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("pk")

        return CollectionNFT.objects.filter(user_id=user_id, is_approved_to_sale=True, user__is_staff=True,
                                            user__is_superuser=False).exclude(user__projectmember=None).all()
