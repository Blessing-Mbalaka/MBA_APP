from django.shortcuts import render, redirect, get_object_or_404
from mbamain.utils.shortcuts import require_auth, require_scholar, require_student, update_module, sdg_goals
from mbamain.models import Project, NoticeToSubmitForm, ResearchInterest
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseForbidden, Http404, HttpResponseNotFound
from django.utils import timezone


@require_auth
@require_student
@update_module
def projects(request):
    interests = ResearchInterest.objects.all()
    SKILLS = [interest.name for interest in interests ]
    per_page = 10
    page = request.GET.get("page", 0)

    try:
        page = int(page)
        if page < 0:
            page = 0
    except:
        page = 0
        
    has_next = True
    next_page = page+1
    prev_page = page -1 if page > 0 else 0

    next_url = reverse("mba_main:projects") + f"?page={next_page}"
    prev_url = reverse("mba_main:projects") + f"?page={prev_page}"
    projects = request.user.projects.all().order_by("project_start_date")[page*per_page:(page+1)*per_page]
    
    if len(projects) == 0 and page > 0: # no more projects on this page, redirect to the previous page
        page = page - 1
        next_url = reverse("mba_main:projects") + f"?page={page}"
        return redirect(next_url)
        
    return render(request, "mbamain/student/projects.html", {"projects": projects, "next":next_url, "prev": prev_url , "has_next": has_next, "has_prev": True if page > 0 else False, "skills": SKILLS, 'GOALS': sdg_goals} )


@require_auth
@require_student
@update_module
def create_project(request):
    if request.method == "POST":
        project_title = request.POST.get("title")
        project_description = request.POST.get("description")
        discipline = request.POST.get("discipline")
        sdg = request.POST.get("sdg")

        # Create a new project instance
        new_project = Project(
            student=request.user,
            project_title=project_title,
            project_description=project_description,
            discipline=discipline,
            sdg_goal = sdg,
        )
        new_project.save()
        messages.success(request, "Project created successfully!")
        return redirect("mba_main:projects")
    
@require_auth
@require_student
@update_module
def update_project(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=project_id)
        if request.user.id != project.student.id:
            return HttpResponseForbidden()
        project_title = request.POST.get("title")
        project_description = request.POST.get("description")
        discipline = request.POST.get("discipline")
        sdg = request.POST.get("sdg")
        
        project.sdg_goal = sdg
        project.project_title = project_title
        project.project_description = project_description
        project.discipline = discipline
        project.save()

        messages.success(request, "Project updated successfully!")
        return redirect("mba_main:projects")
    






@require_auth
@require_student
@update_module
def manage_project(request,id):
    project = get_object_or_404(Project, pk=id)
    if not project.student.id == request.user.id:
        return HttpResponseForbidden()
    return render(request, "mbamain/student/manageProject.html", {"project": project})

@require_auth
@require_scholar
def projects_scholar(request):
    per_page = 10
    page = request.GET.get("page", 0)
    search = request.GET.get("search", '')
    is_searching = True if search and  (not search == '') else False
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0
    search_query = f"&search={search}" if is_searching else ""
    has_next = True
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_main:projects_scholar") + f"?page={next_page}{search_query}"
    prev_url = reverse("mba_main:projects_scholar") + f"?page={prev_page}{search_query}"

    if is_searching:
        projects = Project.objects.all().filter(primary_supervisor=request.user.id, project_title__icontains=search ).order_by("created_date")[page * per_page:(page + 1) * per_page]
    else:
        projects = Project.objects.all().filter( primary_supervisor=request.user.id).order_by("-created_date")[page * per_page:(page + 1) * per_page]
    if len(projects) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_main:projects_scholar") + f"?page={page}{search_query}"
        return redirect(next_url)
    
    return render(request,  "mbamain/scholar/projects.html", {
        "projects": projects,
        "next": next_url,
        "prev": prev_url,
        "has_next": has_next,
        "has_prev": True if page > 0 else False,
        "search": search
    })
   



def notice_to_submit(request,id):
    if request.method == "GET":
     project = get_object_or_404(Project,pk=id)
     student_id = project.student.id
     if request.user.is_student() and not (student_id == request.user.id):
      return HttpResponseForbidden() 
     try:
         form = project.notice_form
     except:
         form = None
     return render(request, "mbamain/academicForms/itentionToSubmitForm.html", {'project': project, "form": form})
    else:
        pass



@require_auth
def submit_notice_form(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        #check if supervisor submitting 
        if not request.user.is_scholar() or request.user.id != project.primary_supervisor:
            return HttpResponseForbidden("You do not have permission to submit this form.")
        if not project.can_submit_notice():
            messages.error(request, "You cannot submit this project notice form. Please ensure that the the two forms form are signed by the student and supervisor.")
            return redirect("mba_main:manage_project", id=project.id)
        project.intent_form_submitted = True
        project.save()
        messages.success(request, "Project notice form submitted successfully.")
        return redirect("mba_main:manage_project", id=project.id)
    return HttpResponseNotFound()

@require_auth
def sign_notice_form(request,project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not project.primary_supervisor:
        messages.error(request, "This project does not have a primary supervisor assigned yet. Please contact the admin to assign a primary supervisor.")
        return redirect('mba_main:notice_form', id= project.id)
    
    if not request.method == "POST":
        raise Http404()
   

    form, created = NoticeToSubmitForm.objects.get_or_create(project=project)

    co_supervisor_details = request.POST.get("co_supervisor_details")
   
    if request.user.is_student(): 
        form.co_supervisor_details= co_supervisor_details
        form.student_signed = True
        form.save()
       
        messages.success(request, "You have successfully signed the notice form")
        return redirect('mba_main:notice_form', id= project.id)
    
    elif request.user.is_scholar() and form:
        supervisor_agree = request.POST.get("supervisorApproval", False)
        supervisor_comment = request.POST.get("comment")
        title_approved = request.POST.get("title_approved", False)
        ethical_clearance_number = request.POST.get("ethics")
        co_supervisor_details = request.POST.get("co_supervisor_details")
        examiners_nominated = request.POST.get("examinersNominatedByMe", False)
        examiners_nominated_approved = request.POST.get("examinersNominated", False)
        form.supervisor_agree = supervisor_agree
        form.co_supervisor_details = co_supervisor_details
        form.supervisors_comment = supervisor_comment
        form.title_approved_hdc = title_approved
        form.approved_hdc = examiners_nominated_approved
        form.ethicals = ethical_clearance_number
        form.nominated_examinners = examiners_nominated
        form.supervisors_signed_date = timezone.now()
        form.supervisor_signed = True
        form.save()
        messages.success(request, "You have successfully signed the notice form")


    return redirect('mba_main:notice_form', id= project.id)

@require_auth
@require_scholar
def scholar_manage_project(request,id):
    project = get_object_or_404(Project, pk=id)
    if not project.primary_supervisor == request.user.id:
      return HttpResponseForbidden()
    return render(request, "mbamain/scholar/manageProject.html", {
        "project": project,
        "student": project.student,
    })


@require_auth
@require_scholar
def submit_to_hdc(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project = get_object_or_404(Project, pk=project_id)
        if not project.primary_supervisor == request.user.id:
            return HttpResponseForbidden()
        if not project.can_submit_hdc():
            messages.error(request, "You cannot submit this project to HDC. Please ensure that  all forms are signed by the student and supervisor.")
            return redirect("mba_main:projects_scholar")
        project.project_status = Project.ProjectStatus.HDC_SUBMITTED
        project.save()
        messages.success(request, "projected successfully submitted to HDC.")
        return redirect("mba_main:projects_scholar")
    