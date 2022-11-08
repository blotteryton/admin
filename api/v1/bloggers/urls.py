from django.urls import path

from api.v1.bloggers.views import BloggerView, BloggerCollectionsView


urlpatterns = [
    path('<int:pk>/', BloggerView.as_view()),
    path('<int:pk>/collections/', BloggerCollectionsView.as_view()),
]
