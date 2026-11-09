"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("views.main.urls")),
    path("", include("views.services.urls")),
    path("", include("views.orders.urls")),
    path("", include("views.inventory.urls")),
    path("", include("views.billing.urls")),
    path("", include("views.accounts.urls")),
]
