from django.urls import path

from api.v1.nfts.views import NftView


urlpatterns = [
    path('<int:pk>/', NftView.as_view()),
]
