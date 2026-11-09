from django.contrib import admin

from views.vehicles.models import Automobilis, Vizitas

admin.site.register([Automobilis, Vizitas])
