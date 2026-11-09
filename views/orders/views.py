from django.shortcuts import get_object_or_404, render

from views.accounts.models import Meistras
from views.main.prototype import prototype_submit
from views.main.roles import Role, get_role, role_required
from views.orders.forms import MeistroUzsakymasForm, UzsakymasForm
from views.orders.models import Uzsakymas
from views.vehicles.models import Vizitas

STAFF = (Role.VADYBININKAS, Role.MEISTRAS)


def _orders_for(user):
    qs = Uzsakymas.objects.select_related(
        "automobilis", "meistras__user", "vadybininkas__user"
    ).prefetch_related("paslaugos")
    if get_role(user) == Role.MEISTRAS:
        qs = qs.filter(meistras=user.meistras)
    return qs


def _initial_from_visit(request):
    """Prefill a new order when created from a visit (?vizitas=<pk>)."""
    vizitas = Vizitas.objects.filter(pk=request.GET.get("vizitas") or None).first()
    if not vizitas:
        return {}
    return {"vizitas": vizitas, "automobilis": vizitas.automobilis}


@role_required(*STAFF)
def order_list(request):
    return render(
        request, "orders/order_list.html", {"orders": _orders_for(request.user)}
    )


@role_required(Role.VADYBININKAS)
def order_create(request):
    if request.method == "POST":
        # full implementation goes here: validate, save Uzsakymas with
        # vadybininkas=request.user.vadybininkas, compute bendra_kaina
        return prototype_submit(request, "orders:order_list")
    return render(
        request,
        "orders/order_form.html",
        {"form": UzsakymasForm(initial=_initial_from_visit(request))},
    )


@role_required(*STAFF)
def order_detail(request, pk):
    order = get_object_or_404(_orders_for(request.user), pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})


@role_required(*STAFF)
def order_edit(request, pk):
    order = get_object_or_404(_orders_for(request.user), pk=pk)
    form_class = (
        UzsakymasForm
        if get_role(request.user) == Role.VADYBININKAS
        else MeistroUzsakymasForm
    )
    if request.method == "POST":
        # full implementation goes here: validate, save, notify client by
        # e-mail when busena changes (El. pašto sąsaja)
        return prototype_submit(request, "orders:order_detail", pk)
    return render(
        request,
        "orders/order_form.html",
        {"form": form_class(instance=order), "order": order},
    )


@role_required(Role.VADYBININKAS)
def assign_master(request, pk):
    order = get_object_or_404(Uzsakymas, pk=pk)
    if request.method == "POST":
        # full implementation goes here: order.meistras = Meistras(pk=POST
        # ["meistras"]), check max_uzsakymu_skaicius, update uzimtas
        return prototype_submit(request, "orders:order_detail", pk)
    masters = Meistras.objects.select_related("user").filter(uzimtas=False)
    return render(
        request, "orders/assign_master.html", {"order": order, "masters": masters}
    )
