from django.shortcuts import get_object_or_404, render

from views.main.prototype import prototype_submit
from views.main.roles import Role, get_role, role_required
from views.vehicles.forms import AutomobilisForm, VizitasForm
from views.vehicles.models import Automobilis, Vizitas

CLIENT_OR_MANAGER = (Role.KLIENTAS, Role.VADYBININKAS)


def _cars_for(user):
    qs = Automobilis.objects.select_related("savininkas__user")
    if get_role(user) == Role.KLIENTAS:
        qs = qs.filter(savininkas=user.klientas)
    return qs


def _visits_for(user):
    qs = Vizitas.objects.select_related("automobilis", "klientas__user")
    if get_role(user) == Role.KLIENTAS:
        qs = qs.filter(klientas=user.klientas)
    return qs


# --- Automobiliai ------------------------------------------------------------


@role_required(*CLIENT_OR_MANAGER)
def car_list(request):
    return render(request, "vehicles/car_list.html", {"cars": _cars_for(request.user)})


@role_required(*CLIENT_OR_MANAGER)
def car_create(request):
    if request.method == "POST":
        # full implementation goes here: validate, verify VIN via external
        # VIN system, save Automobilis(savininkas=request.user.klientas)
        return prototype_submit(request, "vehicles:car_list")
    return render(request, "vehicles/car_form.html", {"form": AutomobilisForm()})


@role_required(*CLIENT_OR_MANAGER)
def car_detail(request, pk):
    car = get_object_or_404(_cars_for(request.user), pk=pk)
    return render(request, "vehicles/car_detail.html", {"car": car})


# --- Vizitai -----------------------------------------------------------------


@role_required(*CLIENT_OR_MANAGER)
def visit_list(request):
    return render(
        request, "vehicles/visit_list.html", {"visits": _visits_for(request.user)}
    )


@role_required(*CLIENT_OR_MANAGER)
def visit_create(request):
    form = VizitasForm(initial=request.GET.dict(), cars=_cars_for(request.user))
    if request.method == "POST":
        # full implementation goes here: validate slot availability, save Vizitas
        return prototype_submit(request, "vehicles:visit_list")
    return render(request, "vehicles/visit_form.html", {"form": form})


@role_required(*CLIENT_OR_MANAGER)
def visit_detail(request, pk):
    visit = get_object_or_404(_visits_for(request.user), pk=pk)
    return render(request, "vehicles/visit_detail.html", {"visit": visit})


@role_required(*CLIENT_OR_MANAGER)
def visit_edit(request, pk):
    visit = get_object_or_404(_visits_for(request.user), pk=pk)
    if request.method == "POST":
        # full implementation goes here: validate, save changes to Vizitas
        return prototype_submit(request, "vehicles:visit_detail", pk)
    form = VizitasForm(instance=visit, cars=_cars_for(request.user))
    return render(request, "vehicles/visit_form.html", {"form": form, "visit": visit})
