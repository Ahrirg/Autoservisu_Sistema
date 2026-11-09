"""User profiles.

``Naudotojas`` from the domain model is Django's built-in ``User`` (vardas,
pavarde, el. paštas, prisijungimo vardas, slaptažodis, sukūrimo data). Each role
is a profile attached one-to-one to it.
"""

from decimal import Decimal

from django.conf import settings
from django.db import models


class Klientas(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="klientas"
    )
    adresas = models.CharField("Adresas", max_length=255, blank=True)
    sutinka_gauti_pranesimus = models.BooleanField(
        "Sutinka gauti pranešimus", default=False
    )

    class Meta:
        verbose_name = "Klientas"
        verbose_name_plural = "Klientai"

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Vadybininkas(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vadybininkas"
    )
    idarbinimo_data = models.DateField("Įdarbinimo data", null=True, blank=True)
    atlyginimas = models.DecimalField(
        "Atlyginimas", max_digits=10, decimal_places=2, default=Decimal("0")
    )
    darbo_telefonas = models.CharField("Darbo telefonas", max_length=32, blank=True)

    class Meta:
        verbose_name = "Vadybininkas"
        verbose_name_plural = "Vadybininkai"

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Meistras(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meistras"
    )
    kvalifikacija = models.CharField("Kvalifikacija", max_length=100, blank=True)
    darbo_stazas = models.PositiveIntegerField("Darbo stažas (m.)", default=0)
    valandinis_ikainis = models.DecimalField(
        "Valandinis įkainis", max_digits=8, decimal_places=2, default=Decimal("0")
    )
    idarbinimo_data = models.DateField("Įdarbinimo data", null=True, blank=True)
    max_uzsakymu_skaicius = models.PositiveIntegerField(
        "Maks. užsakymų skaičius", default=3
    )
    uzimtas = models.BooleanField("Užimtas", default=False)

    class Meta:
        verbose_name = "Meistras"
        verbose_name_plural = "Meistrai"

    def __str__(self):
        return self.user.get_full_name() or self.user.username
