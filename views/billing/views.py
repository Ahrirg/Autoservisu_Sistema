from django.shortcuts import get_object_or_404, render

from views.billing.forms import SaskaitaForm
from views.billing.models import Saskaita
from views.main.prototype import prototype_submit
from views.main.roles import Role, get_role, role_required

CLIENT_OR_MANAGER = (Role.KLIENTAS, Role.VADYBININKAS)


def _invoices_for(user):
    qs = Saskaita.objects.select_related("uzsakymas__automobilis__savininkas__user")
    if get_role(user) == Role.KLIENTAS:
        qs = qs.filter(uzsakymas__automobilis__savininkas=user.klientas)
    return qs


@role_required(*CLIENT_OR_MANAGER)
def invoice_list(request):
    return render(
        request, "billing/invoice_list.html", {"invoices": _invoices_for(request.user)}
    )


@role_required(Role.VADYBININKAS)
def invoice_create(request):
    if request.method == "POST":
        # full implementation goes here: generate saskaitos_nr, compute suma /
        # pvm_suma from Uzsakymas, save Saskaita
        return prototype_submit(request, "billing:invoice_list")
    return render(
        request,
        "billing/invoice_form.html",
        {"form": SaskaitaForm(initial=request.GET.dict())},
    )


@role_required(*CLIENT_OR_MANAGER)
def invoice_detail(request, pk):
    invoice = get_object_or_404(_invoices_for(request.user), pk=pk)
    return render(request, "billing/invoice_detail.html", {"invoice": invoice})


@role_required(Role.VADYBININKAS)
def invoice_edit(request, pk):
    invoice = get_object_or_404(Saskaita, pk=pk)
    if request.method == "POST":
        # full implementation goes here: validate and save Saskaita
        return prototype_submit(request, "billing:invoice_detail", pk)
    return render(
        request,
        "billing/invoice_form.html",
        {"form": SaskaitaForm(instance=invoice), "invoice": invoice},
    )


@role_required(Role.KLIENTAS)
def invoice_pay(request, pk):
    invoice = get_object_or_404(_invoices_for(request.user), pk=pk)
    # full implementation goes here: create Stripe Checkout session, handle
    # webhook -> Mokejimas record, set busena=APMOKETA and apmokejimo_data
    return render(request, "billing/invoice_pay.html", {"invoice": invoice})
