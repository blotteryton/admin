from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy

from NFT_marketplace import settings


admin.site.site_header = 'Blottery'  # default: "Django Administration"
admin.site.index_title = gettext_lazy('Personal Area')  # default: "Site administration"
admin.site.site_title = 'Blottery'  # default: "Django site admin"

urlpatterns = [
    path('', include("users.urls")),
    path('', admin.site.urls, name="account"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
