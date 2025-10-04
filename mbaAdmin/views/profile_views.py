from django.shortcuts import redirect, render
from mbaAdmin.utils import is_admin


@is_admin
def profile(request):
    return render(request, "mbaAdmin/profile.html")