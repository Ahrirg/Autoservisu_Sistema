from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)
from django.contrib.auth.models import User

from views.accounts.models import Klientas, Meistras
from views.main.forms import CarbonFormMixin, DateInput

USER_LABELS = {
    "username": "Pavadinimas",
    "first_name": "Tikrasis vardas",
    "last_name": "Pavardė",
    "email": "El. paštas",
}


class LoginForm(CarbonFormMixin, AuthenticationForm):
    error_messages = {
        "invalid_login": "Neteisingas vardas arba slaptažodis.",
        "inactive": "Ši paskyra neaktyvi.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = USER_LABELS["username"]
        self.fields["password"].label = "Slaptažodis"


class RegisterForm(CarbonFormMixin, UserCreationForm):
    first_name = forms.CharField(label=USER_LABELS["first_name"], max_length=150)
    last_name = forms.CharField(label="Pavardė", max_length=150)
    email = forms.EmailField(label="El. paštas")
    adresas = forms.CharField(label="Adresas", max_length=255, required=False)

    error_messages = {
        **UserCreationForm.error_messages,
        "password_mismatch": "Slaptažodžiai nesutampa.",
    }

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {"username": UsernameField}
        labels = USER_LABELS
        error_messages = {
            "username": {
                "unique": "Naudotojas tokiu vardu jau yra.",
                # UnicodeUsernameValidator (code "invalid")
                "invalid": "Varde gali būti tik raidės, skaičiai "
                "ir simboliai @ . + - _",
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Slaptažodis"
        self.fields["password2"].label = "Pakartokite slaptažodį"

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Klientas.objects.create(user=user, adresas=self.cleaned_data["adresas"])
        return user


class UserForm(CarbonFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
        labels = USER_LABELS


class KlientasForm(CarbonFormMixin, forms.ModelForm):
    class Meta:
        model = Klientas
        fields = ("adresas", "sutinka_gauti_pranesimus")


class MeistrasForm(CarbonFormMixin, forms.ModelForm):
    class Meta:
        model = Meistras
        exclude = ("user",)
        widgets = {"idarbinimo_data": DateInput()}
