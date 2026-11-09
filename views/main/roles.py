"""User roles and role-based access helpers.

A user's role is derived from which profile (``accounts`` app) is attached to the
Django ``User``: ``Klientas``, ``Meistras`` or ``Vadybininkas``.
"""

from collections.abc import Callable
from enum import StrEnum
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


class Role(StrEnum):
    KLIENTAS = "klientas"
    MEISTRAS = "meistras"
    VADYBININKAS = "vadybininkas"

    @property
    def label(self) -> str:
        return {
            Role.KLIENTAS: "Klientas",
            Role.MEISTRAS: "Meistras",
            Role.VADYBININKAS: "Vadybininkas",
        }[self]


def get_role(user) -> Role | None:
    if not user.is_authenticated:
        return None
    for role in Role:
        if hasattr(user, role.value):
            return role
    return None


def role_required(*roles: Role) -> Callable:
    """Require login and (optionally) one of the given roles."""

    def decorator(view: Callable) -> Callable:
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if roles and get_role(request.user) not in roles:
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return login_required(wrapper)

    return decorator
