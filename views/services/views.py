from django.shortcuts import get_object_or_404, render

from views.main.prototype import prototype_submit
from views.main.roles import Role, role_required
from views.services.forms import PaslaugaForm
from views.services.models import Paslauga


@role_required(Role.VADYBININKAS)
def service_list(request):
    return render(
        request, "services/service_list.html", {"services": Paslauga.objects.all()}
    )


@role_required(Role.VADYBININKAS)
def service_create(request):
    if request.method == "POST":
        # full implementation goes here: validate and save Paslauga
        return prototype_submit(request, "services:service_list")
    return render(request, "services/service_form.html", {"form": PaslaugaForm()})


@role_required(Role.VADYBININKAS)
def service_detail(request, pk):
    service = get_object_or_404(Paslauga, pk=pk)
    return render(request, "services/service_detail.html", {"service": service})


@role_required(Role.VADYBININKAS)
def service_edit(request, pk):
    service = get_object_or_404(Paslauga, pk=pk)
    if request.method == "POST":
        # full implementation goes here: validate and save Paslauga
        return prototype_submit(request, "services:service_detail", pk)
    return render(
        request,
        "services/service_form.html",
        {"form": PaslaugaForm(instance=service), "service": service},
    )
