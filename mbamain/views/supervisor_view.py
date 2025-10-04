
from django.shortcuts import render, redirect, get_object_or_404
from mbamain.utils.shortcuts import require_auth, require_student, require_scholar
from mbamain.models import AUser, Project, ExamminerProfile
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden

@require_auth
@require_student
def supervisors(request):
    per_page = 5
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0
    has_next = True
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_main:supervisors") + f"?page={next_page}"
    prev_url = reverse("mba_main:supervisors") + f"?page={prev_page}"
    #to do exlcude those with no profiles
    supervisors = AUser.objects.filter(Q(role_type=AUser.RoleType.SUPERVISOR) | Q(role_type=AUser.RoleType.BOTH)).exclude().order_by("date_joined")[page * per_page:(page + 1) * per_page]
    if len(supervisors) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_main:supervisors") + f"?page={page}"   
        return redirect(next_url)
    
    #get student projects without supervisors
    projects = request.user.projects.filter(primary_supervisor__isnull=True)
    return render(request, "mbamain/student/supervisors.html", {
        "supervisors": supervisors,
        "next": next_url,
        "prev": prev_url,
        "has_next": has_next,
        "has_prev": True if page > 0 else False,
        "projects": projects,
    })


@require_auth
def appoint_assessor(request, assessor_id):
    project_id = request.GET.get('project_id',0)
    project = get_object_or_404(Project, pk=project_id)
    if not project.primary_supervisor == request.user.id:
        return HttpResponseForbidden()
    if not assessor_id in [1,2,3]:
        assessor_id = 1
        return redirect(reverse("mba_main:appoint_assessor", kwargs={"assessor_id": assessor_id}) + f"?project_id={project_id}")
    
    if request.method == "POST":
      examiner_id = request.POST.get("id")
      # check if examminer exists
      if not ExamminerProfile.objects.filter(id=examiner_id).exists():
          messages.error(request, "Examminer does not exist.")
          return redirect(reverse("mba_main:appoint_assessor", kwargs={"assessor_id": assessor_id}) + f"?project_id={project_id}")
      
      if assessor_id == 1:
          project.assessor_1_approved = False
          project.assessor_1_invite_sent = False
          project.assessor_1_responded = False
          project.assessor_1_response = False
          
          project.assessor_1 = examiner_id
          messages.success(request, "Assessor 1 appointed successfully.")
      elif assessor_id == 2:
            project.assessor_2_approved = False
            project.assessor_2_invite_sent = False
            project.assessor_2_responded = False
            project.assessor_2_response = False
            
            messages.success(request, "Assessor 2 appointed successfully.")
            project.assessor_2 = examiner_id
      elif assessor_id == 3:
            
            project.assessor_3_approved = False
            project.assessor_3_invite_sent = False
            project.assessor_3_responded = False
            project.assessor_3_response = False
            
            messages.success(request, "Assessor 3 appointed successfully.")
            project.assessor_3 = examiner_id
      project.save()
      redirect(reverse("mba_main:appoint_assessor", kwargs={"assessor_id": assessor_id}) + f"?project_id={project_id}")

    per_page = 5
    page = request.GET.get("page", 0)
    search = request.GET.get("search", "")
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    if search:
        assessors = ExamminerProfile.objects.filter(
            (Q(name__icontains=search) |
            Q(surname__icontains=search) |
            Q(email__icontains=search) ) & Q(skills__icontains=project.discipline)
        ).order_by('-created_at')[page*per_page:(page+1)*per_page]
    else:
        assessors = ExamminerProfile.objects.filter(skills__icontains=project.discipline).order_by('-created_at')[page*per_page:(page+1)*per_page]
    
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_main:appoint_assessor", kwargs={"assessor_id": assessor_id}) + f"?page={next_page}&project_id={project_id}&search={search}"
    prev_url = reverse("mba_main:appoint_assessor", kwargs={"assessor_id": assessor_id}) + f"?page={prev_page}&project_id={project_id}&search={search}"
    
    if len(assessors) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_main:appoint_assessor", kwargs={"assessor_id": assessor_id}) + f"?page={page}&project_id={project_id}&search={search}"   
        return redirect(next_url)

   
    return  render(request,"mbamain/scholar/examiners.html", {
        "assessors": assessors,
        "next": next_url,
        "prev": prev_url,
        "search": search,
        "project_id": project_id,
         "project": project
        
    
    })