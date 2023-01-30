from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from schemas.views import MyLoginView


urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path("accounts/login/", MyLoginView.as_view()),
    path("accounts/", include("django.contrib.auth.urls")),

    # apps
    path("schemas/", include("schemas.urls")),

    # api
    path("api/schemas/", include("schemas.api.urls")),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
