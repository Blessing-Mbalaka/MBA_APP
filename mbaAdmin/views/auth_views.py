from django.shortcuts import redirect, render
from mbamain.models import AUser
from django.contrib.auth import authenticate, login, logout


def signin(request):
    if request.user.is_authenticated:
        return redirect("mba_admin:index")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
             # If the user is authenticated, redirect to the admin index page
            if user.is_admin():
                login(request, user)  # Log the user in
                return redirect("mba_admin:index")
            elif user.is_hdc():
                login(request, user)  # Log the user in
                return redirect("mba_admin:hdc_titles_submission")
            return render(request, "mbaAdmin/auth/signIn.html", {"error": "You do not have admin access"})
        else:
            return render(request, "mbaAdmin/auth/signIn.html", {"error": "Invalid credentials"})
       
    # If the request method is GET render the sign in page
    return render(request, "mbaAdmin/auth/signIn.html")


def signout(request):
    logout(request)  # Log the user out
    # After logging out, redirect to the sign-in page
    return redirect("mba_admin:signin")