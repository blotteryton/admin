from django.urls import path

from api.v1.collections.views import (CollectionsView, CollectionNewView, CollectionPopularView,
                                      CollectionView, CollectionNftsView)


urlpatterns = [
    path('', CollectionsView.as_view()),
    path('new/', CollectionNewView.as_view()),
    path('popular/', CollectionPopularView.as_view()),
    path('<int:pk>/', CollectionView.as_view()),
    path('<int:pk>/nfts/', CollectionNftsView.as_view()),
]
