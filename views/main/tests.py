"""Smoke tests: every prototype screen renders for the roles allowed to see it."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from views.accounts.models import Meistras
from views.billing.models import Saskaita
from views.inventory.models import Dalis
from views.orders.models import Uzsakymas
from views.services.models import Paslauga
from views.vehicles.models import Automobilis, Vizitas


class PrototypeScreensTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", stdout=StringIO())

    def login(self, username):
        self.assertTrue(self.client.login(username=username, password="pass"))

    def assert_pages_ok(self, urls):
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse("main:dashboard"))
        self.assertRedirects(response, reverse("accounts:login") + "?next=/")

    def test_auth_pages(self):
        self.assert_pages_ok([reverse("accounts:login"), reverse("accounts:register")])

    def test_login_lists_demo_users(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertContains(response, "vadybininkas")

    def test_register_has_no_notifications_consent(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertNotContains(response, "sutinka_gauti_pranesimus")

    def test_register_creates_klientas(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "naujas",
                "first_name": "Naujas",
                "last_name": "Klientas",
                "email": "naujas@example.com",
                "password1": "Sudetingas-Slaptazodis-42",
                "password2": "Sudetingas-Slaptazodis-42",
            },
        )
        self.assertRedirects(response, reverse("main:dashboard"))
        self.assertEqual(self.client.get(reverse("main:dashboard")).status_code, 200)

    def test_invalid_form_uses_carbon_invalid_state(self):
        response = self.client.post(reverse("accounts:register"), {"username": ""})
        self.assertContains(response, "cds--text-input--invalid")
        self.assertContains(response, "cds--form-requirement")

    def test_dashboard_only_greets(self):
        self.login("user1")
        response = self.client.get(reverse("main:dashboard"))
        self.assertContains(response, "Sveiki, Jonas Jonaitis!")
        self.assertContains(response, "UserRole: Klientas")

    def test_klientas_screens(self):
        self.login("user1")
        car = Automobilis.objects.filter(savininkas__user__username="user1")[0]
        visit = Vizitas.objects.filter(klientas__user__username="user1")[0]
        invoice = Saskaita.objects.get(saskaitos_nr="AS-2026-0001")
        self.assert_pages_ok(
            [
                reverse("main:dashboard"),
                reverse("accounts:profile"),
                reverse("accounts:profile_edit"),
                reverse("accounts:profile_delete"),
                reverse("vehicles:car_list"),
                reverse("vehicles:car_create"),
                reverse("vehicles:car_detail", args=[car.pk]),
                reverse("vehicles:visit_list"),
                reverse("vehicles:visit_create"),
                reverse("vehicles:visit_detail", args=[visit.pk]),
                reverse("vehicles:visit_edit", args=[visit.pk]),
                reverse("billing:invoice_list"),
                reverse("billing:invoice_detail", args=[invoice.pk]),
                reverse("billing:invoice_pay", args=[invoice.pk]),
            ]
        )
        # Role restrictions
        self.assertEqual(self.client.get(reverse("orders:order_list")).status_code, 403)
        other_car = Automobilis.objects.exclude(savininkas__user__username="user1")[0]
        response = self.client.get(reverse("vehicles:car_detail", args=[other_car.pk]))
        self.assertEqual(response.status_code, 404)

    def test_meistras_screens(self):
        self.login("meistras")
        order = Uzsakymas.objects.filter(meistras__user__username="meistras")[0]
        part = Dalis.objects.all()[0]
        self.assert_pages_ok(
            [
                reverse("main:dashboard"),
                reverse("orders:order_list"),
                reverse("orders:order_detail", args=[order.pk]),
                reverse("orders:order_edit", args=[order.pk]),
                reverse("inventory:part_list"),
                reverse("inventory:part_detail", args=[part.pk]),
                reverse("inventory:part_edit", args=[part.pk]),
            ]
        )
        self.assertEqual(
            self.client.get(reverse("accounts:employee_list")).status_code, 403
        )

    def test_vadybininkas_screens(self):
        self.login("vadybininkas")
        order = Uzsakymas.objects.filter(vizitas__isnull=False)[0]
        meistras = Meistras.objects.get(user__username="meistras")
        assert order.vizitas is not None
        self.assert_pages_ok(
            [
                reverse("main:dashboard"),
                reverse("accounts:employee_list"),
                reverse("accounts:employee_create"),
                reverse("accounts:employee_detail", args=[meistras.pk]),
                reverse("accounts:employee_edit", args=[meistras.pk]),
                reverse("vehicles:visit_list"),
                reverse("vehicles:visit_detail", args=[Vizitas.objects.all()[0].pk]),
                reverse("vehicles:car_list"),
                reverse("orders:order_list"),
                reverse("orders:order_create"),
                reverse("orders:order_create") + f"?vizitas={order.vizitas.pk}",
                reverse("orders:order_detail", args=[order.pk]),
                reverse("orders:order_edit", args=[order.pk]),
                reverse("orders:assign_master", args=[order.pk]),
                reverse("services:service_list"),
                reverse("services:service_create"),
                reverse("services:service_detail", args=[Paslauga.objects.all()[0].pk]),
                reverse("services:service_edit", args=[Paslauga.objects.all()[0].pk]),
                reverse("inventory:part_list"),
                reverse("inventory:part_create"),
                reverse("billing:invoice_list"),
                reverse("billing:invoice_create"),
                reverse("billing:invoice_detail", args=[Saskaita.objects.all()[0].pk]),
                reverse("billing:invoice_edit", args=[Saskaita.objects.all()[0].pk]),
            ]
        )

    def test_prototype_form_submit_redirects(self):
        self.login("vadybininkas")
        order = Uzsakymas.objects.all()[0]
        response = self.client.post(reverse("orders:order_edit", args=[order.pk]))
        self.assertRedirects(response, reverse("orders:order_detail", args=[order.pk]))
