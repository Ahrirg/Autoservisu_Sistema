from django.urls import path

from views.vehicles import views

app_name = "vehicles"

urlpatterns = [
    path("automobiliai/", views.car_list, name="car_list"),
    path("automobiliai/naujas/", views.car_create, name="car_create"),
    path("automobiliai/<int:pk>/", views.car_detail, name="car_detail"),
    path("vizitai/", views.visit_list, name="visit_list"),
    path("vizitai/naujas/", views.visit_create, name="visit_create"),
    path("vizitai/<int:pk>/", views.visit_detail, name="visit_detail"),
    path("vizitai/<int:pk>/redaguoti/", views.visit_edit, name="visit_edit"),
]
