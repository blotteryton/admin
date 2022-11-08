from django.urls import path

from api.v1.account.views import MeView, TransferView


urlpatterns = [
    path('me/', MeView.as_view()),
    path('transfer/', TransferView.as_view()),
]
