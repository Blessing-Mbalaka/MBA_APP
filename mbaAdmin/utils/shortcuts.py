
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from mbamain.models import AUser, InviteScheduler, Invite
from django.utils import timezone
import threading
from django.shortcuts import redirect, get_object_or_404
from decouple import config
import re

def is_admin(view_fuc):
    def wrapper(request, *args, **kwargs):
        schedule, created = InviteScheduler.objects.get_or_create(created=True)
        if  schedule.should_send():
             t = threading.Thread(target=send_reminders)
             t.start()  # Start the thread to send reminders
        if request.user.is_authenticated and request.user.is_admin():
            return view_fuc(request, *args, **kwargs)
        elif not request.user.is_authenticated:
            return redirect("mba_main:signin")
        else:
            # Redirect authenticated non-admin users to their appropriate dashboard
            if request.user.user_type == AUser.UserType.EXAMINER:
                return redirect("mba_main:profile_examiner")
            elif request.user.is_scholar():
                return redirect("mba_main:index_scholar")
            elif request.user.is_student():
                return redirect("mba_main:index")
            elif request.user.is_hdc():
                return redirect("mba_admin:hdc_titles_submission")
            else:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("You are not allowed to access this page.")
    return wrapper

def is_admin_or_hdc(view_fuc):
    """Allow both ADMIN and HDC users"""
    def wrapper(request, *args, **kwargs):
        schedule, created = InviteScheduler.objects.get_or_create(created=True)
        if  schedule.should_send():
             t = threading.Thread(target=send_reminders)
             t.start()  # Start the thread to send reminders
        if request.user.is_authenticated and (request.user.is_admin() or request.user.is_hdc()):
            return view_fuc(request, *args, **kwargs)
        elif not request.user.is_authenticated:
            return redirect("mba_main:signin")
        else:
            # Redirect authenticated non-admin/hdc users to their appropriate dashboard
            if request.user.user_type == AUser.UserType.EXAMINER:
                return redirect("mba_main:profile_examiner")
            elif request.user.is_scholar():
                return redirect("mba_main:index_scholar")
            elif request.user.is_student():
                return redirect("mba_main:index")
            else:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("You are not allowed to access this page.")
    return wrapper

def is_hdc(view_fuc):
    def wrapper(request, *args, **kwargs):
        schedule, created = InviteScheduler.objects.get_or_create(created=True)
        if  schedule.should_send():
             t = threading.Thread(target=send_reminders)
             t.start()  # Start the thread to send reminders
        if request.user.is_authenticated and request.user.is_hdc():
            return view_fuc(request, *args, **kwargs)
        elif not request.user.is_authenticated:
            return redirect("mba_main:signin")
        else:
            # Redirect authenticated non-HDC users to their appropriate dashboard
            if request.user.is_admin():
                return redirect("mba_admin:index")
            elif request.user.user_type == AUser.UserType.EXAMINER:
                return redirect("mba_main:profile_examiner")
            elif request.user.is_scholar():
                return redirect("mba_main:index_scholar")
            elif request.user.is_student():
                return redirect("mba_main:index")
            else:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("You are not allowed to access this page.")
    return wrapper


def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def valid_role_type(role):    
        return role in [AUser.RoleType.EXAMINER, AUser.RoleType.SUPERVISOR, AUser.RoleType.BOTH]  

def generate_temp_password():
    import random
    import string
    length = 8
    characters = string.ascii_letters + string.digits
    temp_password = ''.join(random.choice(characters) for i in range(length))
    return temp_password


# Discipline-to-Skills Alias Mapping for Smart Supervisor Matching
DISCIPLINE_ALIASES = {
    'Cybersecurity': ['cybersecurity', 'network security', 'information security', 'infosec', 'network architecture', 'security'],
    'Machine Learning': ['machine learning', 'ai', 'artificial intelligence', 'deep learning', 'data science', 'ml'],
    'Cloud Computing': ['cloud computing', 'cloud', 'devops', 'aws', 'azure', 'gcp', 'infrastructure'],
    'Data Science': ['data science', 'data analysis', 'analytics', 'big data', 'data mining', 'statistics'],
    'Business Analytics': ['business analytics', 'analytics', 'business intelligence', 'bi', 'data analytics'],
    'Digital Marketing': ['digital marketing', 'marketing', 'seo', 'smo', 'brand strategy', 'content marketing'],
    'Finance & Banking': ['finance', 'banking', 'financial analysis', 'investment', 'fintech'],
    'Computer Science': ['computer science', 'software development', 'software engineering', 'programming', 'algorithms'],
    'Network Architecture': ['network architecture', 'networking', 'network security', 'cybersecurity', 'infrastructure'],
}


def get_discipline_keywords(discipline):
    """
    Get all alias keywords for a given discipline.
    
    Args:
        discipline (str): The formal discipline name
        
    Returns:
        list: All keyword variants for this discipline (lowercase)
    """
    if not discipline:
        return []
    
    normalized_discipline = discipline.strip()
    
    # Check if exact match exists in aliases
    for key, aliases in DISCIPLINE_ALIASES.items():
        if key.lower() == normalized_discipline.lower():
            return aliases
    
    # If no exact match, try the discipline itself as a keyword
    return [normalized_discipline.lower()]


def supervisor_matches_discipline(supervisor_skills, project_discipline):
    """
    Intelligently check if supervisor skills match the project discipline.
    Uses flexible keyword matching to handle naming variations between
    test data and real discipline names.
    
    Args:
        supervisor_skills (str): Comma-separated skills string from supervisor profile
        project_discipline (str): The project's discipline name
        
    Returns:
        bool: True if supervisor skills match the project discipline
    """
    if not supervisor_skills or not project_discipline:
        return False
    
    # Get all keywords for this discipline
    keywords = get_discipline_keywords(project_discipline)
    
    # Convert supervisor skills to lowercase for case-insensitive matching
    supervisor_skills_lower = supervisor_skills.lower()
    
    # Check if any keyword appears in supervisor skills
    for keyword in keywords:
        if keyword.lower() in supervisor_skills_lower:
            return True
    
    return False


def send_invite(user,temp_password):
    # First, render the plain text content.
    text_content = render_to_string(
        "mbaAdmin/emails/invite.txt",
        context={"email`": user.email,"password": temp_password},
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mbaAdmin/emails/invite.html",
        context={"user": user, "password": temp_password},
    )

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "Welcome, To the MBA System",
        text_content,
        config("EMAIL_HOST_USER"),
        [user.email],
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_appointed(title, email):
    # First, render the plain text content.
    text_content = render_to_string(
        "mbaAdmin/emails/appoinedEmail.txt",
        context={"project_title": title},
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mbaAdmin/emails/appoinedEmail.html",
       context={"project_title": title},
    )

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "New Project Supervision Assignment",
        text_content,
        config("EMAIL_HOST_USER"),
        [email],
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def supervisor_allocated(title, email, project):
    # First, render the plain text content.
    text_content = render_to_string(
        "mbaAdmin/emails/allocatedSupervisor.txt",
        context={"project_title": title, "project": project},
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mbaAdmin/emails/allocatedSupervisor.html",
       context={"project_title": title, "project": project},
    )

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "Supervisor Appointed",
        text_content,
        config("EMAIL_HOST_USER"),
        [email],
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_supervisor_invite(email, project):
      # First, render the plain text content.
    text_content = render_to_string(
        "mbaAdmin/emails/inviteSupervisor.txt",
        context={"project": project},
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mbaAdmin/emails/inviteSupervisor.html",
        context={"project": project},
    )

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "Invitation To Supervise",
        text_content,
        config("EMAIL_HOST_USER"),
        [email],
    
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_assessor_invite_email(email, project):
      # First, render the plain text content.
    text_content = render_to_string(
        "mbaAdmin/emails/inviteAssessor.txt",
        context={"project": project},
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mbaAdmin/emails/inviteAssessor.html",
        context={"project": project},
    )

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "Invitation To Assess",
        text_content,
        config("EMAIL_HOST_USER"),
        [email],
    
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def send_invite_email(email):
     # First, render the plain text content.
    text_content = render_to_string(
        "mbaAdmin/emails/reminder.txt",
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mbaAdmin/emails/reminder.html",   
    )
    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "Action Required: Respond to Supervisor Project Invitations",
        text_content,
        config("EMAIL_HOST_USER"),
        [email],
    
    )
    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_reject_email(email):
     # First, render the plain text content.
    text_content = render_to_string(
        "mbaAdmin/emails/projectReject.txt",
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mbaAdmin/emails/projectReject.html",   
    )
    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "Action Required: Project Rejected By Admin",
        text_content,
        config("EMAIL_HOST_USER"),
        [email],
    
    )
    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()
def project_status_changed_email(email, message):
     # First, render the plain text content.
    text_content = render_to_string(
        "mbaAdmin/emails/projectstatus.txt",context={"message": message},
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mbaAdmin/emails/projectstatus.html",   context={"message": message}
    )
    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "Action Required: Project status changed",
        text_content,
        config("EMAIL_HOST_USER"),
        [email],
    
    )
    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_reminders():
    unread_invites = Invite.objects.filter(read=False)
    for invite in unread_invites:
        user = invite.user
        if not user.is_scholar(): # we only want to remind supervisors
            continue
        diff = timezone.now() - invite.created_at
        # if diff.total_seconds() // 60 >= 1 : # for testing only
        if   diff.days >= 3: 
         if invite.count >= 3:
             invite.delete() # delete the invite after 3 reminders
             continue
         send_invite_email(invite.user.email) 
         invite.created_at = timezone.now() # update the created_at to the current time
         invite.count += 1
         invite.save()
    schedule = get_object_or_404(InviteScheduler, created=True)
    schedule.last_sent_date = timezone.now()
    schedule.save()


def send_project_to_assessor(email, student_no, file):
        # First, render the plain text content.
        text_content = render_to_string(
            "mbaAdmin/emails/projectToAssessor.txt", context={"student_no": student_no}
        )
    
        # Secondly, render the HTML content.
        html_content = render_to_string(
            "mbaAdmin/emails/projectToAssessor.html", context={"student_no": student_no}
        )
    
        # Then, create a multipart email instance.
        msg = EmailMultiAlternatives(
            f"New Project Assigned for Assessment-{student_no}",
            text_content,
            config("EMAIL_HOST_USER"),
            [email],
        
        )
        msg.attach(file.name, file.read(), file.content_type)
        # Lastly, attach the HTML content to the email instance and send.
        msg.attach_alternative(html_content, "text/html")
        msg.send()


