from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from views.accounts.forms import (
    KlientasForm,
    LoginForm,
    MeistrasForm,
    RegisterForm,
    UserForm,
)
from views.accounts.models import Meistras
from views.main.prototype import prototype_submit
from views.main.roles import Role, role_required


class PrisijungimoView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


def register(request):
    if request.user.is_authenticated:
        return redirect("main:dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Registracija sėkminga.")
        return redirect("main:dashboard")
    return render(request, "accounts/register.html", {"form": form})


# --- Naudotojo paskyra ------------------------------------------------------


@role_required()
def profile_detail(request):
    return render(request, "accounts/profile_detail.html")


@role_required()
def profile_edit(request):
    user_form = UserForm(request.POST or None, instance=request.user)
    klientas = getattr(request.user, "klientas", None)
    klientas_form = KlientasForm(instance=klientas) if klientas else None
    if request.method == "POST":
        # full implementation goes here: validate user_form/klientas_form, save both
        return prototype_submit(request, "accounts:profile")
    return render(
        request,
        "accounts/profile_edit.html",
        {"user_form": user_form, "klientas_form": klientas_form},
    )


@role_required()
def profile_delete(request):
    if request.method == "POST":
        # full implementation goes here: anonymise/delete user, logout, redirect
        return prototype_submit(
            request, "main:dashboard", message="Prototipas: paskyra nepašalinta."
        )
    return render(request, "accounts/profile_delete.html")


# --- Darbuotojai (valdo vadybininkas) ---------------------------------------


@role_required(Role.VADYBININKAS)
def employee_list(request):
    meistrai = Meistras.objects.select_related("user").order_by("user__last_name")
    return render(request, "accounts/employee_list.html", {"meistrai": meistrai})


@role_required(Role.VADYBININKAS)
def employee_detail(request, pk):
    meistras = get_object_or_404(Meistras.objects.select_related("user"), pk=pk)
    return render(request, "accounts/employee_detail.html", {"meistras": meistras})


@role_required(Role.VADYBININKAS)
def employee_create(request):
    if request.method == "POST":
        # full implementation goes here: create User + Meistras profile
        return prototype_submit(request, "accounts:employee_list")
    return render(
        request,
        "accounts/employee_form.html",
        {"user_form": UserForm(), "form": MeistrasForm()},
    )


@role_required(Role.VADYBININKAS)
def employee_edit(request, pk):
    meistras = get_object_or_404(Meistras.objects.select_related("user"), pk=pk)
    if request.method == "POST":
        # full implementation goes here: validate and save User + Meistras
        return prototype_submit(request, "accounts:employee_detail", pk)
    return render(
        request,
        "accounts/employee_form.html",
        {
            "meistras": meistras,
            "user_form": UserForm(instance=meistras.user),
            "form": MeistrasForm(instance=meistras),
        },
    )
