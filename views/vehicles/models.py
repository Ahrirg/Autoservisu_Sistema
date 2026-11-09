from django.db import models

from views.accounts.models import Klientas


class Automobilis(models.Model):
    class KuroTipas(models.TextChoices):
        BENZINAS = "benzinas", "Benzinas"
        DYZELIS = "dyzelis", "Dyzelis"
        HIBRIDAS = "hibridas", "Hibridas"
        ELEKTRA = "elektra", "Elektra"
        DUJOS = "dujos", "Dujos"

    savininkas = models.ForeignKey(
        Klientas, on_delete=models.CASCADE, related_name="automobiliai"
    )
    vin = models.CharField("VIN", max_length=17, unique=True)
    valstybinis_nr = models.CharField("Valstybinis Nr.", max_length=16)
    marke = models.CharField("Markė", max_length=64)
    modelis = models.CharField("Modelis", max_length=64)
    pagaminimo_metai = models.PositiveIntegerField("Pagaminimo metai")
    rida = models.PositiveIntegerField("Rida (km)", default=0)
    kuro_tipas = models.CharField(
        "Kuro tipas", max_length=16, choices=KuroTipas.choices
    )
    vin_patikrintas = models.BooleanField("VIN patikrintas", default=False)

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

    def __str__(self):
        return f"{self.marke} {self.modelis} ({self.valstybinis_nr})"


class Vizitas(models.Model):
    class Busena(models.TextChoices):
        REGISTRUOTAS = "registruotas", "Registruotas"
        PATVIRTINTAS = "patvirtintas", "Patvirtintas"
        ATLIKTAS = "atliktas", "Atliktas"
        ATSAUKTAS = "atsauktas", "Atšauktas"

    klientas = models.ForeignKey(
        Klientas, on_delete=models.CASCADE, related_name="vizitai"
    )
    automobilis = models.ForeignKey(
        Automobilis, on_delete=models.CASCADE, related_name="vizitai"
    )
    data = models.DateField("Data")
    laikas = models.TimeField("Laikas")
    problemos_aprasymas = models.TextField("Problemos aprašymas", blank=True)
    busena = models.CharField(
        "Būsena", max_length=16, choices=Busena.choices, default=Busena.REGISTRUOTAS
    )
    sukurimo_data = models.DateTimeField("Sukūrimo data", auto_now_add=True)

    class Meta:
        verbose_name = "Vizitas"
        verbose_name_plural = "Vizitai"
        ordering = ["-data", "-laikas"]

    def __str__(self):
        return f"Vizitas #{self.pk} - {self.data} {self.laikas:%H:%M}"
