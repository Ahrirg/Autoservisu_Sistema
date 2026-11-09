from django.shortcuts import get_object_or_404, render

from views.inventory.forms import DalisForm, LikutisForm
from views.inventory.models import Dalis
from views.main.prototype import prototype_submit
from views.main.roles import Role, get_role, role_required

STAFF = (Role.VADYBININKAS, Role.MEISTRAS)


@role_required(*STAFF)
def part_list(request):
    return render(request, "inventory/part_list.html", {"parts": Dalis.objects.all()})


@role_required(Role.VADYBININKAS)
def part_create(request):
    if request.method == "POST":
        # full implementation goes here: validate and save Dalis
        return prototype_submit(request, "inventory:part_list")
    return render(request, "inventory/part_form.html", {"form": DalisForm()})


@role_required(*STAFF)
def part_detail(request, pk):
    part = get_object_or_404(Dalis, pk=pk)
    return render(request, "inventory/part_detail.html", {"part": part})


@role_required(*STAFF)
def part_edit(request, pk):
    part = get_object_or_404(Dalis, pk=pk)
    if request.method == "POST":
        # full implementation goes here: validate and save Dalis / likutis
        return prototype_submit(request, "inventory:part_detail", pk)
    form_class = (
        DalisForm if get_role(request.user) == Role.VADYBININKAS else LikutisForm
    )
    return render(
        request,
        "inventory/part_form.html",
        {"form": form_class(instance=part), "part": part},
    )
