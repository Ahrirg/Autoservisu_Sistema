from django.db import models


class Dalis(models.Model):
    pavadinimas = models.CharField("Pavadinimas", max_length=128)
    gamintojas = models.CharField("Gamintojas", max_length=64, blank=True)
    katalogo_nr = models.CharField("Katalogo Nr.", max_length=64, unique=True)
    kaina = models.DecimalField("Kaina (€)", max_digits=10, decimal_places=2)
    likutis = models.PositiveIntegerField("Likutis", default=0)
    minimalus_likutis = models.PositiveIntegerField("Minimalus likutis", default=0)
    prognozuojamas_poreikis = models.PositiveIntegerField(
        "Prognozuojamas poreikis", default=0
    )
    vieta = models.CharField("Vieta sandėlyje", max_length=64, blank=True)

    class Meta:
        verbose_name = "Dalis"
        verbose_name_plural = "Dalys"
        ordering = ["pavadinimas"]

    def __str__(self):
        return f"{self.pavadinimas} ({self.katalogo_nr})"

    @property
    def mazas_likutis(self) -> bool:
        return self.likutis <= self.minimalus_likutis
