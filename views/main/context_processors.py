from django.urls import reverse

from views.main.roles import Role, get_role

K, M, V = Role.KLIENTAS, Role.MEISTRAS, Role.VADYBININKAS

# (label, url name, url_name prefix that marks the item active, roles)
NAV_ITEMS = [
    ("Pagrindinis", "main:dashboard", "dashboard", (K, M, V)),
    ("Vizitai", "vehicles:visit_list", "visit_", (K, V)),
    ("Automobiliai", "vehicles:car_list", "car_", (K,)),
    ("Užsakymai", "orders:order_list", "order_", (M, V)),
    ("Darbuotojai", "accounts:employee_list", "employee_", (V,)),
    ("Paslaugos", "services:service_list", "service_", (V,)),
    ("Dalys", "inventory:part_list", "part_", (M, V)),
    ("Sąskaitos", "billing:invoice_list", "invoice_", (K, V)),
]


def user_role(request):
    role = get_role(request.user)
    url_name = getattr(request.resolver_match, "url_name", "") or ""
    nav_items = [
        {
            "label": label,
            "url": reverse(name),
            "active": url_name.startswith(prefix)
            or (prefix == "order_" and url_name.startswith("assign_")),
        }
        for label, name, prefix, roles in NAV_ITEMS
        if role in roles
    ]
    return {
        "role": role,
        "is_klientas": role == K,
        "is_meistras": role == M,
        "is_vadybininkas": role == V,
        "nav_items": nav_items,
    }
