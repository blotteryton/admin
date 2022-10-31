from django.urls import path

from users.views import Register, CreateWallet

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('create_wallet/', CreateWallet.as_view(), name='create_wallet')
]
