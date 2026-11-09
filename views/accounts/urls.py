from django.contrib.auth.views import LogoutView
from django.urls import path

from views.accounts import views

app_name = "accounts"

urlpatterns = [
    path("prisijungti/", views.PrisijungimoView.as_view(), name="login"),
    path("atsijungti/", LogoutView.as_view(), name="logout"),
    path("registruotis/", views.register, name="register"),
    path("paskyra/", views.profile_detail, name="profile"),
    path("paskyra/redaguoti/", views.profile_edit, name="profile_edit"),
    path("paskyra/salinti/", views.profile_delete, name="profile_delete"),
    path("darbuotojai/", views.employee_list, name="employee_list"),
    path("darbuotojai/naujas/", views.employee_create, name="employee_create"),
    path("darbuotojai/<int:pk>/", views.employee_detail, name="employee_detail"),
    path("darbuotojai/<int:pk>/redaguoti/", views.employee_edit, name="employee_edit"),
]
