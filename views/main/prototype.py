"""Helpers for the UI prototype: form submissions navigate but don't persist."""

from django.contrib import messages
from django.shortcuts import redirect


def prototype_submit(request, to, *args, message="Prototipas: duomenys neišsaugoti."):
    # full implementation goes here: validate form, form.save(), domain side effects
    messages.info(request, message)
    return redirect(to, *args)
