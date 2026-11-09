from django import forms

from views.billing.models import Saskaita
from views.main.forms import CarbonFormMixin, DateInput


class SaskaitaForm(CarbonFormMixin, forms.ModelForm):
    class Meta:
        model = Saskaita
        exclude = ("apmokejimo_data",)
        widgets = {
            "israsymo_data": DateInput(),
            "apmokejimo_terminas": DateInput(),
        }
