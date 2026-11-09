from django.db import models

from views.orders.models import Uzsakymas


class Saskaita(models.Model):
    class Busena(models.TextChoices):
        NEAPMOKETA = "neapmoketa", "Neapmokėta"
        APMOKETA = "apmoketa", "Apmokėta"
        ATSAUKTA = "atsaukta", "Atšaukta"

    saskaitos_nr = models.CharField("Sąskaitos Nr.", max_length=32, unique=True)
    uzsakymas = models.OneToOneField(
        Uzsakymas, on_delete=models.PROTECT, related_name="saskaita"
    )
    israsymo_data = models.DateField("Išrašymo data")
    apmokejimo_terminas = models.DateField("Apmokėjimo terminas")
    suma = models.DecimalField("Suma (€)", max_digits=10, decimal_places=2)
    pvm_suma = models.DecimalField("PVM suma (€)", max_digits=10, decimal_places=2)
    busena = models.CharField(
        "Būsena", max_length=16, choices=Busena.choices, default=Busena.NEAPMOKETA
    )
    apmokejimo_data = models.DateField("Apmokėjimo data", null=True, blank=True)

    class Meta:
        verbose_name = "Sąskaita"
        verbose_name_plural = "Sąskaitos"
        ordering = ["-israsymo_data"]

    def __str__(self):
        return self.saskaitos_nr

    @property
    def suma_su_pvm(self):
        return self.suma + self.pvm_suma
