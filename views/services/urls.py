from django.urls import path

from views.services import views

app_name = "services"

urlpatterns = [
    path("paslaugos/", views.service_list, name="service_list"),
    path("paslaugos/nauja/", views.service_create, name="service_create"),
    path("paslaugos/<int:pk>/", views.service_detail, name="service_detail"),
    path("paslaugos/<int:pk>/redaguoti/", views.service_edit, name="service_edit"),
]
