from django import forms

from views.main.forms import CarbonFormMixin
from views.services.models import Paslauga


class PaslaugaForm(CarbonFormMixin, forms.ModelForm):
    class Meta:
        model = Paslauga
        fields = "__all__"
        widgets = {"aprasymas": forms.Textarea(attrs={"rows": 4})}
