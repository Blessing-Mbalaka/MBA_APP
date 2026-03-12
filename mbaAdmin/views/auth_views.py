from django.shortcuts import redirect, render
from mbamain.models import AUser
from django.contrib.auth import logout


def signout(request):
    logout(request)  # Log the user out
    # Redirect to main signin page
    return redirect("mba_main:signin")