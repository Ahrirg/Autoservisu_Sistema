from django.urls import path

from views.inventory import views

app_name = "inventory"

urlpatterns = [
    path("dalys/", views.part_list, name="part_list"),
    path("dalys/nauja/", views.part_create, name="part_create"),
    path("dalys/<int:pk>/", views.part_detail, name="part_detail"),
    path("dalys/<int:pk>/redaguoti/", views.part_edit, name="part_edit"),
]
