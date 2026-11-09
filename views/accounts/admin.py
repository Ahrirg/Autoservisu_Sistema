from django.contrib import admin

from views.accounts.models import Klientas, Meistras, Vadybininkas

admin.site.register([Klientas, Vadybininkas, Meistras])
