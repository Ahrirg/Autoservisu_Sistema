from django.urls import path

from views.orders import views

app_name = "orders"

urlpatterns = [
    path("uzsakymai/", views.order_list, name="order_list"),
    path("uzsakymai/naujas/", views.order_create, name="order_create"),
    path("uzsakymai/<int:pk>/", views.order_detail, name="order_detail"),
    path("uzsakymai/<int:pk>/redaguoti/", views.order_edit, name="order_edit"),
    path(
        "uzsakymai/<int:pk>/priskirti-meistra/",
        views.assign_master,
        name="assign_master",
    ),
]
