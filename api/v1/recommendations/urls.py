from django.urls import path

from api.v1.recommendations.views import RecommendationsView

urlpatterns = [
    path('', RecommendationsView.as_view()),
]
