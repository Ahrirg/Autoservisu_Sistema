from django.db import models


class Paslauga(models.Model):
    pavadinimas = models.CharField("Pavadinimas", max_length=128)
    aprasymas = models.TextField("Aprašymas", blank=True)
    kaina = models.DecimalField("Kaina (€)", max_digits=10, decimal_places=2)
    trukme_valandomis = models.DecimalField(
        "Trukmė (val.)", max_digits=5, decimal_places=1
    )
    reikalinga_kvalifikacija = models.CharField(
        "Reikalinga kvalifikacija", max_length=100, blank=True
    )

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"
        ordering = ["pavadinimas"]

    def __str__(self):
        return self.pavadinimas
