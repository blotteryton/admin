from django.urls import path, include

from users.views import Register, CreateWallet

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', Register.as_view(), name='register'),
    path('create_wallet/', CreateWallet.as_view(), name='create_wallet')
]
