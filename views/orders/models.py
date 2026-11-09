from decimal import Decimal

from django.db import models

from views.accounts.models import Meistras, Vadybininkas
from views.services.models import Paslauga
from views.vehicles.models import Automobilis, Vizitas


class Uzsakymas(models.Model):
    class Busena(models.TextChoices):
        NAUJAS = "naujas", "Naujas"
        VYKDOMAS = "vykdomas", "Vykdomas"
        LAUKIA_DALIU = "laukia_daliu", "Laukia dalių"
        ATLIKTAS = "atliktas", "Atliktas"

    automobilis = models.ForeignKey(
        Automobilis, on_delete=models.PROTECT, related_name="uzsakymai"
    )
    vizitas = models.ForeignKey(
        Vizitas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uzsakymai",
    )
    vadybininkas = models.ForeignKey(
        Vadybininkas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uzsakymai",
    )
    meistras = models.ForeignKey(
        Meistras,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uzsakymai",
    )
    paslaugos = models.ManyToManyField(
        Paslauga, verbose_name="Paslaugos", blank=True, related_name="uzsakymai"
    )
    sukurimo_data = models.DateTimeField("Sukūrimo data", auto_now_add=True)
    planuojama_pabaigos_data = models.DateField(
        "Planuojama pabaigos data", null=True, blank=True
    )
    busena = models.CharField(
        "Būsena", max_length=16, choices=Busena.choices, default=Busena.NAUJAS
    )
    bendra_kaina = models.DecimalField(
        "Bendra kaina (€)", max_digits=10, decimal_places=2, default=Decimal("0")
    )
    pastaba = models.TextField("Pastaba", blank=True)

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"
        ordering = ["-sukurimo_data"]

    def __str__(self):
        return f"Užsakymas #{self.pk}"
