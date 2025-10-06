
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import re
from mbamain.models import AUser as User

@require_http_methods(["GET", "POST"])
@csrf_protect
def create_user_view(request):
    """
    Production-ready view for creating AUser instances
    Handles both GET (form display) and POST (form submission)
    """
    
    if request.method == 'GET':
        return render(request, 'mbaAdmin/createUser.html')
    

    # Extract form data
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '')
    password_confirm = request.POST.get('password_confirm', '')
    user_type = request.POST.get('user_type', '3')  # Default to STUDENT
    
    # Validation checks
    errors = []
    
    
    if not email:
        errors.append("Email is required")
    if not password:
        errors.append("Password is required")
    
    
    # Email validation
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append("Please enter a valid email address")
    
    # Password validation
    if password and password_confirm and password != password_confirm:
        errors.append("Passwords do not match")

    
    # User type validation
    try:
        user_type_int = int(user_type)
        valid_user_types = [choice[0] for choice in User.UserType.choices]
        if user_type_int not in valid_user_types:
            errors.append("Invalid user type selected")
    except (ValueError, TypeError):
        errors.append("Invalid user type")
    
    
    
    # If there are validation errors, return to form with errors
    if errors:
        for error in errors:
            messages.error(request, error)
        return render(request, 'mbaAdmin/createUser.html', {
            'form_data': request.POST
        })
    
    # Create user
    try:

        # check if user with email or username already exists

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'mbaAdmin/createUser.html', {
                'form_data': request.POST
            })
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'mbaAdmin/createUser.html', {
                'form_data': request.POST
            })
        


        user = User(
            username=email,
            email=email,
            user_type=user_type_int,
        )
        
        # Set password
        user.set_password(password)
        user.save()
        
        # Success message
        messages.success(request, f"User '{username}' created successfully!")
        
        # Redirect to success page or clear form
        return redirect('mba_admin:create_user')  # You'll need to define this URL
        
    except IntegrityError:
        messages.error(request, "Username or email already exists")
        return render(request, 'createUser.html', {
            'form_data': request.POST
        })
    except Exception as e:
        messages.error(request, "An unexpected error occurred while creating the user")
        return render(request, 'createUser.html', {
            'form_data': request.POST
        })


