from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from api.v1.notifications.serializers import NotificationSerializer
from notification.models import Notification


User = get_user_model()


class NotificationListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.order_by("-id").all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('category',)
