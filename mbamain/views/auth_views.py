from django.shortcuts import redirect, render
from mbamain.models import AUser, PasswordResetToken
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden, Http404
from django.utils import timezone
from mbamain.utils import send_reset_token
import threading


def signin(request):
    if request.user.is_authenticated:
        return redirect("mba_main:index")
    if request.method == "POST":
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        user = authenticate(request, username=email, password=password)
        print(user)
        print(email)
        print(password)
        if user is not None:
            if  user.is_student() and user.get_weeks() > 8:
                logout(request)  # Log the user out if they are not within the allowed weeks
                return redirect("mba_main:update_module")
            login(request, user)  # Log the user in
            if user.is_student():
                return redirect("mba_main:index")
            elif user.is_scholar():
                return redirect("mba_main:index_scholar")
            elif user.is_examiner():
               return redirect("mba_main:profile_examiner")
            elif user.is_hdc():
                return redirect("mba_admin:hdc_titles_submission")
            else:
                return redirect("mba_admin:index") # this is for admin users
        else:
            return render(request, "mbamain/auth/signIn.html", {"error": "Invalid credentials"})
    return render(request, "mbamain/auth/signIn.html")

def signout(request):
    logout(request)  # Log the user out
    return redirect("mba_main:signin")


def signup(request):
    if request.user.is_authenticated:
        return redirect("mba_main:index")
     
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_passowrd = request.POST.get("confirm_password")
        if password != confirm_passowrd:
            # Handle password mismatch
            return render(request, 'mbamain/auth/signUp.html', {'error': 'Passwords do not match'})
        if AUser.objects.filter(email=email).exists():
            # Handle email already exists
            return render(request, 'mbamain/auth/signUp.html', {'error': 'Email already exists'})
        user = AUser.objects.create_user(email=email, password=password, username=email)
        user.save() # save student to the database
        user = authenticate(request, username=email, password=password)  #use username to authenticate the user not their email
        if user is not None:
            login(request, user)  # Log the user in
            return redirect("mba_main:index")
        else:
            # Handle authentication failure
            return render(request, 'mbamain/auth/signUp.html', {'error': 'Authentication failed'})
    return render(request, 'mbamain/auth/signUp.html')



def reset_password(request):
    if request.method == "POST":
      token = request.POST.get("token").strip()
      email  = request.POST.get("email").strip()
      password =  request.POST.get("password").strip()
      confirm_password = request.POST.get("confirm_password").strip()
      if password != confirm_password:
        return render(request, "mbamain/auth/updatePassword.html", {"error": "Passwords do not match"})
      user = AUser.objects.filter(email=email).first()
      if not user:
        return render(request, "mbamain/auth/updatePassword.html", {"error": "A user with the provided email does not exist"})
      reset_token = PasswordResetToken.objects.filter(token=token, user=user).first()
      print(reset_token)
      if not reset_token:
          raise Http404()
      if reset_token.has_expired():
          return render(request, "mbamain/auth/updatePassword.html", {"error": "reset token has already expired, restart the processs"})
      if not reset_token.token == token:
          return render(request, "mbamain/auth/updatePassword.html", {"error": "invalid token"})
      user.set_password(password)
      user.save()
      reset_token.delete()
      user = authenticate(request, username=user.username, password=password)
      
      login(request, user)
      if user.is_student():
         return redirect("mba_main:index")
      elif user.is_scholar():
         return redirect("mba_main:index_scholar")
      elif user.is_examiner():
               return redirect("mba_main:profile_examiner")
      else:
           return redirect("mba_admin:index") # this is for admin users
    return render(request, "mbamain/auth/updatePassword.html")


def get_reset_token(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = AUser.objects.filter(email=email).first()
        if not user:
            return render(request, "mbamain/auth/getResetToken.html", {"error": "A user with the provided email does not exist"})
        reset_token = PasswordResetToken.objects.filter(user=user).first()
        if not reset_token:
          reset_token = PasswordResetToken.objects.create(user=user, token=PasswordResetToken.generate_token(), created_date=timezone.now(), max_time=60)
        else:
            reset_token.token = PasswordResetToken.generate_token()
            reset_token.created_date = timezone.now()
            reset_token.save()
        print("printing token")
        print(reset_token.token)
        t  = threading.Thread(target=send_reset_token, args=(email, reset_token.token))
        t.start()
        return redirect("mba_main:reset_password")
    return render(request, "mbamain/auth/getResetToken.html")