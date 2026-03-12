from django.shortcuts import redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from mbamain.models import AUser, Invite
from django.http import HttpResponseForbidden, Http404

def require_auth(view_func):
    def _wraped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if  request.user.is_admin():
                return redirect("mba_admin:index") # the admin should not access the main app directly
            else:
                return view_func(request, *args, **kwargs)
        else:
            return redirect("mba_main:signin")
    return _wraped_view

def require_student(view_func):
    def _wrapped_view(request, *args, **kwargs):
        print("User:", request.user)
        if request.user.is_authenticated and request.user.is_student():
            return view_func(request, *args, **kwargs)
        elif request.user.is_authenticated and request.user.is_scholar():
            return redirect("mba_main:profile_scholar")
        elif request.user.is_authenticated and request.user.user_type == AUser.UserType.EXAMINER:
            return redirect("mba_main:profile_examiner")
        elif request.user.is_authenticated and request.user.is_hdc():
            return redirect("mba_admin:hdc_titles_submission")
        else:
            raise Http404()
    return _wrapped_view

def update_module(view_func):
    def _wrapped_view(request, *args, **kwargs):
        weeks = request.user.get_weeks()
        if weeks > 8:
            return redirect("mba_main:update_module")
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view


def require_scholar(view_func):
 def _wrapped_view(request, *args, **kwargs):    
        if request.user.is_authenticated and request.user.is_scholar():
            return view_func(request, *args, **kwargs)
        else:
            raise Http404()
 return _wrapped_view

def require_examiner(view_func):
 def _wrapped_view(request, *args, **kwargs):    
        if request.user.is_authenticated and request.user.user_type == AUser.UserType.EXAMINER:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404()
 return _wrapped_view


def send_reset_token(email, token):
    # First, render the plain text content.
    text_content = render_to_string(
        "mbamain/emails/passwordChange.txt",
        context={"token": token},
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mbamain/emails/passwordChange.html",
        context={"token": token},
    )

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "Password Reset Token",
        text_content,
        "mbasystem@euj.ac.za",
        [email],
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()




def clean_title(title):
    words = title.split()

    if not (len(words) <= 15):
        return None  # Invalid title

    formatted = title.lower().capitalize()
    return formatted

SKILLS = [
    "Leadership",
    "Business",
    "Economics",
    "Maths",
    "Researcher",
    "Agriculture",
    "Entrepreneurship",
    "Project Management",
    "HR",
    "Organisational Behavior",
    "HSE",
    "Change Management",
    "Psychology",
    "Education",
    "Management",
    "Strategy",
    "Marketing",
    "Supply Chain",
    "Finance",
    "Hospitality",
    "Human Capital Development",
    "Governance",
    "SME",
    "Strategic Management",
    "Technology"
]


sdg_goals = [
    "No Poverty",
    "Zero Hunger",
    "Good Health and Well-being",
    "Quality Education",
    "Gender Equality",
    "Clean Water and Sanitation",
    "Affordable and Clean Energy",
    "Decent Work and Economic Growth",
    "Industry, Innovation and Infrastructure",
    "Reduced Inequalities",
    "Sustainable Cities and Communities",
    "Responsible Consumption and Production",
    "Climate Action",
    "Life Below Water",
    "Life on Land",
    "Peace, Justice and Strong Institutions",
    "Partnerships for the Goals"
]
