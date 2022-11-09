from django.urls import path

from api.v1.notifications.views import NotificationListView


urlpatterns = [
    path('', NotificationListView.as_view()),
]
