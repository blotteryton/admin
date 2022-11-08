from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, authentication

from NFT_marketplace import settings


admin.site.site_header = 'Blottery'  # default: "Django Administration"
admin.site.index_title = gettext_lazy('Personal Area')  # default: "Site administration"
admin.site.site_title = 'Blottery'  # default: "Django site admin"


schema_view = get_schema_view(
    openapi.Info(
       title="Blottery API",
       default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[authentication.TokenAuthentication],
)


urlpatterns = [
    path('api/', include("api.urls")),
    path('account/', admin.site.urls, name="account"),
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
