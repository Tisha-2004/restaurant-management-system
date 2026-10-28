from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("customers/", include("customers.urls")),
    path("menu/", include("menu.urls")),
    path("tables/", include("tables.urls")),
    path("reservation/", include("reservations.urls")),
    path("kitchen/", include("kitchen.urls")),
    path("billing/", include("billing.urls")),
    path("reports/", include("reports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")

handler404 = "core.views.handler404"
handler500 = "core.views.handler500"
