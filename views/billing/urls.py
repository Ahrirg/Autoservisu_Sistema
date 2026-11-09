from django.urls import path

from views.billing import views

app_name = "billing"

urlpatterns = [
    path("saskaitos/", views.invoice_list, name="invoice_list"),
    path("saskaitos/nauja/", views.invoice_create, name="invoice_create"),
    path("saskaitos/<int:pk>/", views.invoice_detail, name="invoice_detail"),
    path("saskaitos/<int:pk>/redaguoti/", views.invoice_edit, name="invoice_edit"),
    path("saskaitos/<int:pk>/apmoketi/", views.invoice_pay, name="invoice_pay"),
]
