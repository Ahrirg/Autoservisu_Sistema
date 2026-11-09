from django.shortcuts import render

from views.main.roles import role_required


@role_required()
def dashboard(request):
    return render(request, "main/dashboard.html")
