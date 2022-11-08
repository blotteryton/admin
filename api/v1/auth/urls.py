from django.urls import path

from api.v1.auth.views import GetTokenView


urlpatterns = [
    path('token/', GetTokenView.as_view()),
]
