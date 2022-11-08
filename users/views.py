from django.shortcuts import redirect
from django.views import View

from users.utils import create_wallet


class CreateWallet(View):
    def get(self, request):
        create_wallet(user=self.request.user)
        return redirect(request.META.get('HTTP_REFERER', '/'))
