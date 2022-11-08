from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, get_object_or_404

from administration.models import MarketplaceConfiguration
from api.v1.recommendations.serializers import RecommendationsSerializer


User = get_user_model()


class RecommendationsView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = RecommendationsSerializer
    queryset = MarketplaceConfiguration.get_solo()

    def get_object(self):
        return self.get_queryset()
