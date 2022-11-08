from django.urls import path, include

urlpatterns = [
    path('auth/', include("api.v1.auth.urls")),
    path('account/', include("api.v1.account.urls")),
    path('bloggers/', include("api.v1.bloggers.urls")),
    path('collections/', include("api.v1.collections.urls")),
    path('nfts/', include("api.v1.nfts.urls")),
    path('recommendations/', include("api.v1.recommendations.urls")),
]
