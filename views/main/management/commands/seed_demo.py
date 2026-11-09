"""Populate the database with demo users and data for the UI prototype.

Usage: uv run python manage.py seed_demo
Idempotent: re-running updates/keeps existing records.
"""

import datetime as dt
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from views.accounts.models import Klientas, Meistras, Vadybininkas
from views.billing.models import Saskaita
from views.inventory.models import Dalis
from views.orders.models import Uzsakymas
from views.services.models import Paslauga
from views.vehicles.models import Automobilis, Vizitas

PASSWORD = "pass"


def make_user(username, first, last, *, superuser=False):
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={
            "first_name": first,
            "last_name": last,
            "email": f"{username}@autoservisas.lt",
        },
    )
    user.set_password(PASSWORD)  # bypasses password validators on purpose (demo)
    user.is_staff = user.is_superuser = superuser
    user.save()
    return user


class Command(BaseCommand):
    help = "Create demo users (password 'pass') and sample data."

    @transaction.atomic
    def handle(self, *args, **options):
        today = dt.date.today()

        make_user("admin", "Admin", "Adminas", superuser=True)

        # --- Users / roles ---------------------------------------------------
        k1, _ = Klientas.objects.get_or_create(
            user=make_user("user1", "Jonas", "Jonaitis"),
            defaults={"adresas": "Gedimino pr. 1, Vilnius"},
        )
        k2, _ = Klientas.objects.get_or_create(
            user=make_user("user2", "Ona", "Onaitė"),
            defaults={"adresas": "Laisvės al. 10, Kaunas"},
        )
        vad, _ = Vadybininkas.objects.get_or_create(
            user=make_user("vadybininkas", "Rasa", "Rasaitė"),
            defaults={
                "idarbinimo_data": dt.date(2021, 3, 1),
                "atlyginimas": Decimal("2100"),
                "darbo_telefonas": "+37060000001",
            },
        )
        m1, _ = Meistras.objects.get_or_create(
            user=make_user("meistras", "Petras", "Petraitis"),
            defaults={
                "kvalifikacija": "Variklių remontas",
                "darbo_stazas": 8,
                "valandinis_ikainis": Decimal("35"),
                "idarbinimo_data": dt.date(2019, 5, 1),
                "uzimtas": True,
            },
        )
        Meistras.objects.get_or_create(
            user=make_user("meistras2", "Tomas", "Tomaitis"),
            defaults={
                "kvalifikacija": "Elektronika ir diagnostika",
                "darbo_stazas": 4,
                "valandinis_ikainis": Decimal("30"),
                "idarbinimo_data": dt.date(2022, 9, 1),
            },
        )
        Meistras.objects.get_or_create(
            user=make_user("meistras3", "Lukas", "Lukaitis"),
            defaults={
                "kvalifikacija": "Važiuoklė ir stabdžiai",
                "darbo_stazas": 2,
                "valandinis_ikainis": Decimal("25"),
                "idarbinimo_data": dt.date(2024, 1, 15),
            },
        )

        # --- Catalogue -------------------------------------------------------
        services = {}
        for name, price, hours, qual in [
            ("Tepalų keitimas", "45.00", "0.5", ""),
            ("Stabdžių kaladėlių keitimas", "80.00", "1.5", "Važiuoklė ir stabdžiai"),
            ("Kompiuterinė diagnostika", "35.00", "1.0", "Elektronika ir diagnostika"),
            ("Paskirstymo diržo keitimas", "320.00", "4.0", "Variklių remontas"),
        ]:
            services[name], _ = Paslauga.objects.get_or_create(
                pavadinimas=name,
                defaults={
                    "kaina": Decimal(price),
                    "trukme_valandomis": Decimal(hours),
                    "reikalinga_kvalifikacija": qual,
                    "aprasymas": f"{name} - standartinė paslauga.",
                },
            )

        for name, maker, cat, price, stock, minimum, place in [
            ("Tepalo filtras", "Mann", "W712/95", "8.50", 24, 10, "A-1"),
            (
                "Variklio alyva 5W-30 (5 l)",
                "Castrol",
                "EDGE-5W30-5L",
                "42.00",
                6,
                8,
                "A-2",
            ),
            ("Stabdžių kaladėlės (priekis)", "Brembo", "P85020", "55.00", 4, 4, "B-3"),
            (
                "Paskirstymo diržo komplektas",
                "Gates",
                "K015578XS",
                "140.00",
                2,
                1,
                "C-1",
            ),
        ]:
            Dalis.objects.get_or_create(
                katalogo_nr=cat,
                defaults={
                    "pavadinimas": name,
                    "gamintojas": maker,
                    "kaina": Decimal(price),
                    "likutis": stock,
                    "minimalus_likutis": minimum,
                    "vieta": place,
                },
            )

        # --- Cars / visits / orders / invoices -------------------------------
        car1, _ = Automobilis.objects.get_or_create(
            vin="WVWZZZ1KZAW000001",
            defaults={
                "savininkas": k1,
                "valstybinis_nr": "ABC123",
                "marke": "Volkswagen",
                "modelis": "Golf",
                "pagaminimo_metai": 2012,
                "rida": 210000,
                "kuro_tipas": Automobilis.KuroTipas.DYZELIS,
                "vin_patikrintas": True,
            },
        )
        car2, _ = Automobilis.objects.get_or_create(
            vin="JTDKB20U093000002",
            defaults={
                "savininkas": k1,
                "valstybinis_nr": "KLM456",
                "marke": "Toyota",
                "modelis": "Prius",
                "pagaminimo_metai": 2018,
                "rida": 95000,
                "kuro_tipas": Automobilis.KuroTipas.HIBRIDAS,
            },
        )
        car3, _ = Automobilis.objects.get_or_create(
            vin="WBA3A5C50DF000003",
            defaults={
                "savininkas": k2,
                "valstybinis_nr": "XYZ789",
                "marke": "BMW",
                "modelis": "320d",
                "pagaminimo_metai": 2015,
                "rida": 160000,
                "kuro_tipas": Automobilis.KuroTipas.DYZELIS,
            },
        )

        if not Vizitas.objects.exists():
            v1 = Vizitas.objects.create(
                klientas=k1,
                automobilis=car1,
                data=today - dt.timedelta(days=3),
                laikas=dt.time(9, 0),
                problemos_aprasymas="Girdisi cypimas stabdant.",
                busena=Vizitas.Busena.PATVIRTINTAS,
            )
            Vizitas.objects.create(
                klientas=k1,
                automobilis=car2,
                data=today + dt.timedelta(days=5),
                laikas=dt.time(13, 30),
                problemos_aprasymas="Planinis tepalų keitimas.",
            )
            v3 = Vizitas.objects.create(
                klientas=k2,
                automobilis=car3,
                data=today - dt.timedelta(days=10),
                laikas=dt.time(11, 0),
                problemos_aprasymas="Dega variklio lemputė.",
                busena=Vizitas.Busena.ATLIKTAS,
            )

            o1 = Uzsakymas.objects.create(
                automobilis=car1,
                vizitas=v1,
                vadybininkas=vad,
                meistras=m1,
                planuojama_pabaigos_data=today + dt.timedelta(days=1),
                busena=Uzsakymas.Busena.VYKDOMAS,
                bendra_kaina=Decimal("80.00"),
            )
            o1.paslaugos.add(services["Stabdžių kaladėlių keitimas"])

            o2 = Uzsakymas.objects.create(
                automobilis=car3,
                vizitas=v3,
                vadybininkas=vad,
                meistras=m1,
                planuojama_pabaigos_data=today - dt.timedelta(days=8),
                busena=Uzsakymas.Busena.ATLIKTAS,
                bendra_kaina=Decimal("355.00"),
                pastaba="Pakeistas paskirstymo diržas, atlikta diagnostika.",
            )
            o2.paslaugos.add(
                services["Kompiuterinė diagnostika"],
                services["Paskirstymo diržo keitimas"],
            )

            o3 = Uzsakymas.objects.create(
                automobilis=car1,
                vadybininkas=vad,
                planuojama_pabaigos_data=today - dt.timedelta(days=30),
                busena=Uzsakymas.Busena.ATLIKTAS,
                bendra_kaina=Decimal("45.00"),
            )
            o3.paslaugos.add(services["Tepalų keitimas"])

            Saskaita.objects.create(
                saskaitos_nr="AS-2026-0001",
                uzsakymas=o3,
                israsymo_data=today - dt.timedelta(days=30),
                apmokejimo_terminas=today + dt.timedelta(days=14),
                suma=Decimal("37.19"),
                pvm_suma=Decimal("7.81"),
            )
            Saskaita.objects.create(
                saskaitos_nr="AS-2026-0002",
                uzsakymas=o2,
                israsymo_data=today - dt.timedelta(days=8),
                apmokejimo_terminas=today + dt.timedelta(days=6),
                suma=Decimal("293.39"),
                pvm_suma=Decimal("61.61"),
                busena=Saskaita.Busena.APMOKETA,
                apmokejimo_data=today - dt.timedelta(days=2),
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data ready. Users (password 'pass'): user1, user2 (klientai), "
                "vadybininkas, meistras, meistras2, meistras3, admin (superuser)."
            )
        )
