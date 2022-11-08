from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from api.v1.auth.serializers import GetTokenSerializer, GetTokenParamsSerializer
from users.utils import create_wallet


User = get_user_model()


@method_decorator(name='get', decorator=swagger_auto_schema(query_serializer=GetTokenParamsSerializer()))
class GetTokenView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = GetTokenSerializer
    queryset = Token.objects.all()

    def get_object(self):
        telegram_id = self.request.query_params.get("user_uid")
        try:
            token = self.queryset.get(user__telegram_id=telegram_id)
        except Token.DoesNotExist:
            try:
                user = User.objects.get(telegram_id=telegram_id)
            except User.DoesNotExist:
                user = User(username=telegram_id, telegram_id=telegram_id)
                user.save()

            token = Token.objects.create(user=user)

            if not user.wallet_address:
                create_wallet(user)

        return {"token": token.key}
