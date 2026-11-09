from django import forms

from views.main.forms import CarbonFormMixin, DateInput
from views.orders.models import Uzsakymas


class UzsakymasForm(CarbonFormMixin, forms.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = (
            "automobilis",
            "vizitas",
            "paslaugos",
            "planuojama_pabaigos_data",
            "busena",
            "pastaba",
        )
        widgets = {
            "paslaugos": forms.CheckboxSelectMultiple(),
            "planuojama_pabaigos_data": DateInput(),
            "pastaba": forms.Textarea(attrs={"rows": 3}),
        }


class MeistroUzsakymasForm(CarbonFormMixin, forms.ModelForm):
    """What a mechanic may change on an assigned order."""

    class Meta:
        model = Uzsakymas
        fields = ("busena", "pastaba")
        widgets = {"pastaba": forms.Textarea(attrs={"rows": 3})}
