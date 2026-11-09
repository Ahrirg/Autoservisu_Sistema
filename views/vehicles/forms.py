from django import forms

from views.main.forms import CarbonFormMixin, DateInput, TimeInput
from views.vehicles.models import Automobilis, Vizitas


class AutomobilisForm(CarbonFormMixin, forms.ModelForm):
    class Meta:
        model = Automobilis
        fields = (
            "vin",
            "valstybinis_nr",
            "marke",
            "modelis",
            "pagaminimo_metai",
            "rida",
            "kuro_tipas",
        )


class VizitasForm(CarbonFormMixin, forms.ModelForm):
    class Meta:
        model = Vizitas
        fields = ("automobilis", "data", "laikas", "problemos_aprasymas")
        widgets = {
            "data": DateInput(),
            "laikas": TimeInput(),
            "problemos_aprasymas": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, cars=None, **kwargs):
        super().__init__(*args, **kwargs)
        if cars is not None:
            field = self.fields["automobilis"]
            assert isinstance(field, forms.ModelChoiceField)
            field.queryset = cars
