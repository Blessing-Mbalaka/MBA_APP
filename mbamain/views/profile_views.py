import json
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from mbamain.utils.shortcuts import require_auth,require_student, require_scholar, update_module, require_examiner
from django.contrib import messages
from mbamain.models import ResearchInterest, ExamminerProfile , StudentProfile, SupervisorProfile
from django.contrib.auth import authenticate, login


@require_auth
@require_student
@update_module
def profile(request):
    try:
        profile = request.user.student_profile
    except:
        profile = None

    return render(request, "mbamain/student/profile.html", {"user": request.user, "profile": profile, })

@require_auth
@require_scholar
def profile_scholar(request):
    interests = ResearchInterest.objects.all()
    SKILLS = [interest.name for interest in interests ]
    try:
        profile = request.user.supervisor_profile
        skills = profile.skills.split(",") if profile.skills else []
    except:
        profile = None
        skills = []
    # remove skills in SKILLs that are part of skills
    optionsSkills = [skill for skill in SKILLS if skill not in skills]
    
    skills = [{"name": skill, "id": id } for id, skill in enumerate(skills)]
    return render(request, "mbamain/scholar/profile.html", {"user": request.user, "profile": profile,  'skills': skills, "optionsSkills": optionsSkills, "size": len(optionsSkills)})

@require_auth
@require_examiner
def profile_examiner(request):
    interests = ResearchInterest.objects.all()
    SKILLS = [interest.name for interest in interests ]
    try:
        profile = request.user.examiner_profile
        skills = profile.skills.split(",") if profile.skills else []
    except:
        profile = None
        skills = []
    print("skills")
    print(skills)
    # remove skills in SKILLs that are part of skills
    optionsSkills = [skill for skill in SKILLS if skill not in skills]
    skills = [{"name": skill, "id": id } for id, skill in enumerate(skills)]
    return render(request, "mbamain/examiner/profile.html", {"user": request.user, "profile": profile, 'skills': skills, "optionsSkills": optionsSkills, "size": len(optionsSkills)})


@require_auth
@update_module
def update_profile(request):
    if request.method == "POST":
        if request.user.is_student():
            profile = request.user.student_profile
            title = request.POST.get("title")
            name = request.POST.get("name")
            surname = request.POST.get("surname")
            contact = request.POST.get("contact")
            secondary_email = request.POST.get("secondary_email")
            
            profile.title = title
            profile.name = name
            profile.surname = surname
            profile.contact = contact
            profile.secondary_email = secondary_email
            profile.save()
        elif request.user.is_scholar():
            profile = request.user.supervisor_profile
            title = request.POST.get("title")
            name = request.POST.get("name")
            surname = request.POST.get("surname")
            contact  = request.POST.get("contact")
            position = request.POST.get("position")
            skills = request.POST.get("skills")
            profile.title = title
            profile.name = name
            profile.surname = surname
            profile.contact = contact
            profile.position = position
            profile.skills = skills
            profile.save()
        url = "mba_main:profile_scholar" if request.user.is_scholar() else "mba_main:profile"
        messages.success(request, "Profile updated successfully")
        return redirect(url)
    return HttpResponseNotFound()
       

@require_examiner
def update_examiner_profile(request):
    user = request.user  # The logged-in user

    try:
        profile = user.examiner_profile
    except ExamminerProfile.DoesNotExist:
        messages.error(request, "Profile does not exist for this user.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == "POST":
        # Get form data
        profile.title = request.POST.get('title', '').strip()
        profile.name = request.POST.get('name', '').strip()
        profile.surname = request.POST.get('surname', '').strip()
        profile.cell_phone = request.POST.get('cell_phone', '').strip()
        profile.affiliation = request.POST.get('affiliation', '').strip()
        profile.street_address = request.POST.get('street_address', '').strip()
        profile.qualification = request.POST.get('qualification', '').strip()
        profile.current_affiliation = request.POST.get('current_affiliation', '').strip()

     
        try:
            profile.number_of_students_supervised = int(request.POST.get('number_of_students_supervised', 0))
        except ValueError:
            profile.number_of_students_supervised = 0

        try:
            profile.number_publications = int(request.POST.get('number_publications', 0))
        except ValueError:
            profile.number_publications = 0

        try:
            profile.academic_experience = int(request.POST.get('academic_experience', 0))
        except ValueError:
            profile.academic_experience = 0

     
      
        # Save profile
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # If GET request, render the same page or redirect
    messages.error(request, "Invalid request method.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def update_student_profile(request):
    user = request.user  # logged-in user

    try:
        profile = user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile does not exist for this user.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == "POST":
        # Text fields
        profile.title = request.POST.get('title', '').strip()
        profile.name = request.POST.get('name', '').strip()
        profile.surname = request.POST.get('surname', '').strip()
        profile.contact = request.POST.get('contact_number', '').strip()
        profile.secondary_email = request.POST.get('secondary_email', '').strip()
        profile.module = request.POST.get('module', profile.module)
        profile.address = request.POST.get('address', profile.address)
        profile.save()
        messages.success(request, "Student profile updated successfully.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    
    messages.error(request, "Invalid request method.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def update_supervisor_profile(request):
    try:
       
        profile, created = SupervisorProfile.objects.get_or_create(user=request.user)

        if request.method == "POST":
            profile.title = request.POST.get("title", profile.title)
            profile.name = request.POST.get("name", profile.name)
            profile.surname = request.POST.get("surname", profile.surname)
            profile.contact = request.POST.get("contact", profile.contact)
            profile.skills = request.POST.get("skills", profile.skills)
            profile.address = request.POST.get("address", profile.address)
            profile.department = request.POST.get("department", profile.department)
            profile.position = request.POST.get("position", profile.position)
         

            profile.save()
            messages.success(request, "Supervisor profile updated successfully.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # If GET request, just render a page or return JSON/modal content
        context = {"user": request.user}
        return render(request, "mba_main/supervisor_profile_modal.html", context)

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect(request.META.get("HTTP_REFERER", "/"))


@require_auth
def add_interest(request):
    if request.method == "POST":
     skills = request.POST.getlist("skills")
     if request.user.is_scholar():
         userSkills = request.user.supervisor_profile.skills.split(",") if request.user.supervisor_profile.skills else []
         newSkills = [skill for skill in skills if skill not in userSkills]
         request.user.supervisor_profile.skills = ",".join(userSkills + newSkills)
         request.user.supervisor_profile.save()
         messages.success(request, "Skills updated successfully")
         return redirect("mba_main:profile_scholar")
     elif request.user.is_examiner():
         userSkills = request.user.examiner_profile.skills.split(",") if request.user.examiner_profile.skills else []
         newSkills = [skill for skill in skills if skill not in userSkills]
         request.user.examiner_profile.skills = ",".join(userSkills + newSkills)
         request.user.examiner_profile.save()    
     messages.success(request, "Skills updated successfully")
     return redirect("mba_main:profile_examiner")
    return HttpResponseNotFound()

@require_auth
def remove_interest(request):
    if request.method == "POST":
      skill = request.POST.get("skill")
      if request.user.is_scholar():
        request.user.supervisor_profile.skills = ",".join(
            [s for s in request.user.supervisor_profile.skills.split(",") if s != skill]
        )
        request.user.supervisor_profile.save()
        messages.success(request, "Removed successfully")
        return redirect("mba_main:profile_shoclar")
      elif request.user.is_examiner():
        request.user.examiner_profile.skills = ",".join(
            [s for s in request.user.examiner_profile.skills.split(",") if s != skill]
        )
        request.user.examiner_profile.save()
        messages.success(request, "Removed successfully")
        return redirect("mba_main:profile_examiner")
    return HttpResponseNotFound()

def get_interests(request):
    if request.method == "GET":
        per_page = 5
        page = request.GET.get("page", 0)
        search = request.GET.get("search", '')
        try:
            page = int(page)
            if page < 0:
                page = 0
        except ValueError:
            page = 0
        search_query = f"&search={search}"
        next_page = page + 1
        prev_page = page - 1 if page > 0 else 0
        next_url = reverse("mba_main:research_interest_search") + f"?page={next_page}{search_query}" 
        prev_url = reverse("mba_main:research_interest_search") + f"?page={prev_page}{search_query}" if page > 0 else None
        research_interests = ResearchInterest.objects.all().filter(name__icontains=search).order_by("-created_at")[page * per_page:(page + 1) * per_page]
      
        if len(research_interests) == 0 and page > 0:
            page = page - 1
            research_interests = ResearchInterest.objects.all().filter(name__icontains=search).order_by("-created_at")[page * per_page:(page + 1) * per_page]
            next_url = None
            
        
        return JsonResponse({
            "interests": list(research_interests.values()),
            "next": next_url,
            "prev": prev_url,
            "search": search
        })
    else:
        return HttpResponseNotFound()
    




def update_module(request):
    if request.method == "POST":
        module_name = request.POST.get("module_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_student():
            user.student_profile.module = module_name
            user.student_profile.save()
            messages.success(request, "Module updated successfully")
            login(request, user)  # Log the user in
            return redirect("mba_main:index")
        else:
            messages.error(request, "Invalid credentials or user is not a student")
            return redirect("mba_main:update_module")
    return render(request, "mbamain/student/updateModule.html")