from django.urls import path

from users.views import CreateWallet
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(extra_context={"title": "Login", "text_center": "Login"},
                               template_name="auth/login.html",
                               redirect_authenticated_user=True), name='login'),
    path('create_wallet/', CreateWallet.as_view(), name='create_wallet'),
]
