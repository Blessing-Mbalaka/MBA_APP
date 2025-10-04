from mbaAdmin.utils.shortcuts import is_admin, is_hdc, send_reject_email, project_status_changed_email
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.http import HttpResponseNotFound
from mbamain.models import Project, Cv
from django.db.models import Q
from django.contrib import messages
import threading

@is_admin
def hdc(request):
    per_page = 10
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
    block_id = request.GET.get("block_id", '')
    if student_no and block_id:
        filter = (
            Q(student__student_profile__student_no = student_no) & Q(student__student_profile__block_id =block_id)
        )
    elif block_id:
        filter = Q(student__student_profile__block_id = block_id)
    elif student_no:
        filter = Q(student__student_profile__student_no = student_no)
    else:
        filter = Q()
    projects = Project.objects.filter(
        filter,
        project_status=Project.ProjectStatus.HDC_SUBMITTED
    ).order_by("-created_date")[per_page*page:(per_page*(page+1))]
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_admin:hdc") +  f"?page={next_page}&student_no={student_no}&block_id={block_id}"
    prev_url =reverse("mba_admin:hdc") +  f"?page={prev_page}&student_no={student_no}&block_id={block_id}"

    if len(projects) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_admin:hdc") + f"?page={page}&student_no={student_no}&block_id={block_id}"
        return redirect(next_url)
    
    return render(request, "mbaAdmin/hdc.html", {
        "projects": projects,
        "page": page,
        "per_page": per_page,
        "student_no": student_no,
        "block_id": block_id,
        "next": next_url,
        "prev": prev_url,
    })


@is_admin
def titles_submissions(request):
    per_page = 10
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
    block_id = request.GET.get("block_id", '')
    if student_no and block_id:
        filter = (
            Q(student__student_profile__student_no = student_no) & Q(student__student_profile__block_id =block_id)
        )
    elif block_id:
        filter = Q(student__student_profile__block_id = block_id)
    elif student_no:
        filter = Q(student__student_profile__student_no = student_no)
    else:
        filter = Q()
    projects = Project.objects.filter(
        filter,
        Q(project_status=Project.ProjectStatus.JBS5_submitted) | Q(project_status=Project.ProjectStatus.JBS5_HDC_approved)
    ).order_by("-created_date")[per_page*page:(per_page*(page+1))]
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_admin:titles_submitted") +  f"?page={next_page}&student_no={student_no}&block_id={block_id}"
    prev_url =reverse("mba_admin:titles_submitted") +  f"?page={prev_page}&student_no={student_no}&block_id={block_id}"

    if len(projects) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_admin:titles_submitted") + f"?page={page}&student_no={student_no}&block_id={block_id}"
        return redirect(next_url)
    
    return render(request, "mbaAdmin/titlesSubmissions.html", {
        "projects": projects,
        "page": page,
        "per_page": per_page,
        "student_no": student_no,
        "block_id": block_id,
        "next": next_url,
        "prev": prev_url,
    })


@is_admin
def intent_submissions(request):
    per_page = 10
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
    block_id = request.GET.get("block_id", '')
    if student_no and block_id:
        filter = (
            Q(student__student_profile__student_no = student_no) & Q(student__student_profile__block_id =block_id)
        )
    elif block_id:
        filter = Q(student__student_profile__block_id = block_id)
    elif student_no:
        filter = Q(student__student_profile__student_no = student_no)
    else:
        filter = Q()
    projects = Project.objects.filter(
        filter,
        Q(intent_form_submitted=True)
    ).order_by("-created_date")[per_page*page:(per_page*(page+1))]
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_admin:intent_submitted") +  f"?page={next_page}&student_no={student_no}&block_id={block_id}"
    prev_url =reverse("mba_admin:intent_submitted") +  f"?page={prev_page}&student_no={student_no}&block_id={block_id}"

    if len(projects) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_admin:intent_submitted") + f"?page={page}&student_no={student_no}&block_id={block_id}"
        return redirect(next_url)
    
    return render(request, "mbaAdmin/intentSubmissions.html", {
        "projects": projects,
        "page": page,
        "per_page": per_page,
        "student_no": student_no,
        "block_id": block_id,
        "next": next_url,
        "prev": prev_url,
    })


@is_hdc
def hdc_intent_submissions(request):
    per_page = 10
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
    block_id = request.GET.get("block_id", '')
    if student_no and block_id:
        filter = (
            Q(student__student_profile__student_no = student_no) & Q(student__student_profile__block_id =block_id)
        )
    elif block_id:
        filter = Q(student__student_profile__block_id = block_id)
    elif student_no:
        filter = Q(student__student_profile__student_no = student_no)
    else:
        filter = Q()
    projects = Project.objects.filter(
        filter,
        Q(intent_form_submitted=True) & Q(intent_form_approved=False)
    ).order_by("-created_date")[per_page*page:(per_page*(page+1))]
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_admin:hdc_intent_submission") +  f"?page={next_page}&student_no={student_no}&block_id={block_id}"
    prev_url =reverse("mba_admin:hdc_intent_submission") +  f"?page={prev_page}&student_no={student_no}&block_id={block_id}"

    if len(projects) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_admin:hdc_intent_submission") + f"?page={page}&student_no={student_no}&block_id={block_id}"
        return redirect(next_url)
    
    return render(request, "mbaAdmin/hdc/intents.html", {
        "projects": projects,
        "page": page,
        "per_page": per_page,
        "student_no": student_no,
        "block_id": block_id,
        "next": next_url,
        "prev": prev_url,
    })


@is_admin
def approved_hdc(request):
    per_page = 10
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
    block_id = request.GET.get("block_id", '')
    if student_no and block_id:
        filter = (
            Q(student__student_profile__student_no = student_no) & Q(student__student_profile__block_id =block_id)
        )
    elif block_id:
        filter = Q(student__student_profile__block_id = block_id)
    elif student_no:
        filter = Q(student__student_profile__student_no = student_no)
    else:
        filter = Q()
    projects = Project.objects.filter(
        filter,
        (Q(project_status=Project.ProjectStatus.HDC_APPROVED) | Q(project_status=Project.ProjectStatus.HDC_VERIFIED))
    ).order_by("-created_date")[per_page*page:(per_page*(page+1))]
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_admin:approved_hdc") +  f"?page={next_page}&student_no={student_no}"
    prev_url =reverse("mba_admin:approved_hdc") +  f"?page={prev_page}&student_no={student_no}"

    if len(projects) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_admin:approved_hdc") + f"?page={page}&student_no={student_no}"
        return redirect(next_url)
    
    return render(request, "mbaAdmin/approvedHDC.html", {
        "projects": projects,
        "page": page,
        "per_page": per_page,
        "student_no": student_no,
        "block_id": block_id,
        "next": next_url,
        "prev": prev_url,
    })

@is_admin
def nominations_submitted(request):
    per_page = 10
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
    block_id = request.GET.get("block_id", '')
    if student_no and block_id:
        filter = (
            Q(student__student_profile__student_no = student_no) & Q(student__student_profile__block_id =block_id)
        )
    elif block_id:
        filter = Q(student__student_profile__block_id = block_id)
    elif student_no:
        filter = Q(student__student_profile__student_no = student_no)
    else:
        filter = Q()
    projects = Project.objects.filter(
        filter,
        (Q(nomination_form_submitted=True) | Q(nomination_form_hdc_verified = True))
    ).order_by("-created_date")[per_page*page:(per_page*(page+1))]
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_admin:nomination_submitted") +  f"?page={next_page}&student_no={student_no}"
    prev_url =reverse("mba_admin:nomination_submitted") +  f"?page={prev_page}&student_no={student_no}"

    if len(projects) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_admin:nomination_submitted") + f"?page={page}&student_no={student_no}"
        return redirect(next_url)
    
    return render(request, "mbaAdmin/NominationsSubmissions.html", {
        "projects": projects,
        "page": page,
        "per_page": per_page,
        "student_no": student_no,
        "block_id": block_id,
        "next": next_url,
        "prev": prev_url,
    })



@is_hdc
def decline_intent(request):
    project_id = request.POST.get("project_id")
    comment = request.POST.get("comment")
    project = get_object_or_404(Project, pk=project_id)
    if comment.strip():       
        if project.comments:
            project_comments = project.comments
            project_comments = project_comments + "***" + comment
            project.comments = project_comments
        else:
            project.comments = comment
    project.intent_form_submitted = False
    t = threading.Thread(target=project_status_changed_email, args=(project.get_supervisor().email, "Your project intent form has been declined by HDC.",))
    t.start()
    messages.success(request, "Project intent declined successfully")
    project.save()
    return redirect("mba_admin:hdc_intent_submission")

@is_hdc
def approve_intent(request):
    project_id = request.POST.get("project_id")
    project = get_object_or_404(Project, pk=project_id)
    project.intent_form_approved = True
    messages.success(request, "Project intent approved successfully")
    t = threading.Thread(target=project_status_changed_email, args=(project.get_supervisor().email, "Your project intent form has been approved by HDC.",))
    t.start()
    project.save()
    return redirect("mba_admin:hdc_intent_submission")

@is_hdc
def hdc_nomination_submission(request):
    per_page = 10
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
    block_id = request.GET.get("block_id", '')
    if student_no and block_id:
        filter = (
            Q(student__student_profile__student_no = student_no) & Q(student__student_profile__block_id =block_id)
        )
    elif block_id:
        filter = Q(student__student_profile__block_id = block_id)
    elif student_no:
        filter = Q(student__student_profile__student_no = student_no)
    else:
        filter = Q()
    projects = Project.objects.filter(
        filter,
        nomination_form_submitted=True, nomination_form_hdc_verified = False
    ).order_by("-created_date")[per_page*page:(per_page*(page+1))]
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_admin:hdc_nominations") +  f"?page={next_page}&student_no={student_no}"
    prev_url =reverse("mba_admin:hdc_nominations") +  f"?page={prev_page}&student_no={student_no}"

    if len(projects) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_admin:hdc_nominations") + f"?page={page}&student_no={student_no}"
        return redirect(next_url)
    
    return render(request, "mbaAdmin/hdc/hdcView.html", {
        "projects": projects,
        "page": page,
        "per_page": per_page,
        "student_no": student_no,
        "block_id": block_id,
        "next": next_url,
        "prev": prev_url,
    })


@is_hdc
def hdc_titles_submission(request):
    per_page = 10
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
    block_id = request.GET.get("block_id", '')
    if student_no and block_id:
        filter = (
            Q(student__student_profile__student_no = student_no) & Q(student__student_profile__block_id =block_id)
        )
    elif block_id:
        filter = Q(student__student_profile__block_id = block_id)
    elif student_no:
        filter = Q(student__student_profile__student_no = student_no)
    else:
        filter = Q()
    projects = Project.objects.filter(
        filter,
        project_status=Project.ProjectStatus.JBS5_Admin_approved
    ).order_by("-created_date")[per_page*page:(per_page*(page+1))]
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_admin:hdc_titles_submission") +  f"?page={next_page}&student_no={student_no}"
    prev_url =reverse("mba_admin:hdc_titles_submission") +  f"?page={prev_page}&student_no={student_no}"

    if len(projects) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_admin:hdc_titles_submission") + f"?page={page}&student_no={student_no}"
        return redirect(next_url)
    
    return render(request, "mbaAdmin/hdc/hdcViewTitles.html", {
        "projects": projects,
        "page": page,
        "per_page": per_page,
        "student_no": student_no,
        "block_id": block_id,
        "next": next_url,
        "prev": prev_url,
    })






@is_admin
def hdc_approve(request):
    project_id = request.POST.get("project_id")
    project = get_object_or_404(Project, pk=project_id)
    project.project_status = project.ProjectStatus.HDC_APPROVED
    project.save()
    return redirect("mba_admin:hdc")


@is_admin
def hdc_reject(request):
    project_id = request.POST.get("project_id")
    comment = request.POST.get("comment")
    project = get_object_or_404(Project, pk=project_id)
    if comment.strip():       
        if project.comments:
            project_comments = project.comments
            project_comments = project_comments + "***" + comment
            project.comments = project_comments
        else:
            project.comments = comment
    print(project.get_supervisor().email)
    t = threading.Thread(target=send_reject_email, args=(project.get_supervisor().email,))
    t.start()
    project.project_status = project.ProjectStatus.HDC_DECLINED
    project.save()
    return redirect("mba_admin:hdc")
   


@is_admin
def download_cv(request):
    if request.method == "GET":
        try: 
            cv_id = request.GET.get("id")
            cv = get_object_or_404(Cv, pk=cv_id).cv_file
            file_path = cv.path
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{cv.name}"'
                return response
        except Exception as e:
            messages.error(request, f"An error occurred while downloading the CV - {str(e)}")
            return redirect("mba_admin:approved_hdc")






# for hdc only 
@is_hdc
def approve_assessor(request):
    assessor_no = int(request.GET.get("assessor"))
    project_id = request.GET.get("project")
    if not assessor_no in [1,2,3]:
        return HttpResponseNotFound()
    project = get_object_or_404(Project, pk=project_id)
    if assessor_no == 1:
        project.assessor_1_approved = True
        assessor = project.get_assessor_1()
        assessor.approved_before = True
        assessor.save()
    
    elif assessor_no == 2:
        project.assessor_2_approved = True
        assessor = project.get_assessor_2()
        assessor.approved_before = True
        assessor.save()
    elif assessor_no == 3:
        assessor = project.get_assessor_3()
        assessor.approved_before = True
        assessor.save()
        project.assessor_3_approved = True
    project.save()
    messages.success(request, f"Assessor {assessor_no} approved successfully")
    return redirect("mba_admin:hdc_nominations")


@is_hdc
def decline_intent(request):
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
  
    url = reverse("mba_admin:hdc_intents_submission") +  f"?page={page}&student_no={student_no}"
    project_id = request.POST.get("project_id")
    comment = request.POST.get("comment")
    
    if not comment.strip():
        messages.error(request, "Please provide a comment for declining the title.")
        return redirect(url)
    project = get_object_or_404(Project, pk=project_id)
    if comment.strip():
        if project.comments:
            project_comments = project.comments
            project_comments = project_comments + "***" + comment
            project.comments = project_comments
        else:
            project.comments = comment
        project.intent_form_submitted = False
        project.save()
        messages.success(request, "Project title declined successfully")
    return redirect(url)


@is_hdc
def approve_intent(request):
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0
    student_no = request.GET.get("student_no", '')
    url = reverse("mba_admin:hdc_intent_submission") +  f"?page={page}&student_no={student_no}"
    project_id = request.POST.get("project_id")
    project = get_object_or_404(Project, pk=project_id)
    project.intent_form_approved = True
    messages.success(request, "Project intent approved successfully")
    project.save()
    return redirect(url)


@is_hdc
def approve_title(request):
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
  
    url = reverse("mba_admin:hdc_titles_submission") +  f"?page={page}&student_no={student_no}"
    project_id = request.POST.get("project_id")
    project = get_object_or_404(Project, pk=project_id)
    project.project_status = project.ProjectStatus.JBS5_HDC_approved
    project.title_approved = True
    messages.success(request, "Project title approved successfully")
    t = threading.Thread(target=project_status_changed_email, args=(project.student.email, "Your project title has been approved by  HDC. "))
    t.start()
    t = threading.Thread(target=project_status_changed_email, args=(project.get_supervisor().email, f"The project title for student {project.student.email} has been approved by HDC"))
    t.start()
    project.save()

   
    return redirect(url)

@is_hdc
def decline_title(request):
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
  
    url = reverse("mba_admin:hdc_titles_submission") +  f"?page={page}&student_no={student_no}"
    project_id = request.POST.get("project_id")
    comment = request.POST.get("comment")
    
    if not comment.strip():
        messages.error(request, "Please provide a comment for declining the title.")
        return redirect(url)
    project = get_object_or_404(Project, pk=project_id)
    if comment.strip():
        if project.comments:
            project_comments = project.comments
            project_comments = project_comments + "***" + comment
            project.comments = project_comments
        else:
            project.comments = comment
        project.project_status = project.ProjectStatus.JBS5_HDC_declined
        t = threading.Thread(target=project_status_changed_email, args=(project.student.email, "Your project title has been declined by  HDC. "))
        t.start()
        t = threading.Thread(target=project_status_changed_email, args=(project.get_supervisor().email, f"The project title for student {project.student.email} has been declined by HDC"))
        t.start()
        project.save()
        messages.success(request, "Project title declined successfully")
    return redirect(url)



@is_hdc
def decline_assessor(request):
    assessor_no = int(request.GET.get("assessor"))
    project_id = request.GET.get("project")
    if not assessor_no in [1,2,3]:
        return HttpResponseNotFound()
    project = get_object_or_404(Project, pk=project_id)
    if assessor_no == 1:
        project.assessor_1_approved = False
    elif assessor_no == 2:
        project.assessor_2_approved = False
    elif assessor_no == 3:
        project.assessor_3_approved = False
    project.save()
    messages.success(request, f"Assessor {assessor_no} declined successfully")
    return redirect("mba_admin:hdc_nominations")


@is_hdc
def hdc_add_comment(request):
    project_id = request.POST.get("project_id")
    comment = request.POST.get("comment")
    project = get_object_or_404(Project, pk=project_id)
    print(comment)
    if comment.strip():       
        if project.hdc_comments:
            project_comments = project.hdc_comments
            project_comments = project_comments + "***" + comment
            project.hdc_comments = project_comments
        else:
            project.hdc_comments = comment

        project.save()
        messages.success(request, "Comment added successfully")
    else:
        messages.error(request, "Comment cannot be empty")
    return redirect("mba_admin:hdc_nominations")


@is_hdc
def send_project_to_admin(request):
    project_id = request.GET.get("project_id")
    project = get_object_or_404(Project, pk=project_id)
    project.nomination_form_hdc_verified = True
    project.save()
    messages.success(request, "Project sent to admin successfully")
    return redirect("mba_admin:hdc_nominations")



@is_hdc
def hdc_approve_title(request):
    project_id = request.GET.get("project_id")
    project = get_object_or_404(Project, pk=project_id)
    project.project_status = Project.ProjectStatus.JBS5_HDC_approved
    project.title_approved = True
    project.project_title = project.jbs5_form.title
    t = threading.Thread(target=project_status_changed_email, args=(project.student.email, "Your project title has been approved by HDC.",))
    t.start()
    print("project title accepted")
    project.save()
    messages.success(request, "Project title approved successfully")
    return redirect("mba_admin:hdc_titles_submission")




@is_admin
def send_project_to_supervisor(request):
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
  
    url = reverse("mba_admin:nomination_submitted") +  f"?page={page}&student_no={student_no}"
    project_id = request.POST.get("project_id")
    project_id = request.POST.get("project_id")
    comment = request.POST.get("comment")
    project = get_object_or_404(Project, pk=project_id)
    if comment.strip():       
        if project.comments:
            project_comments = project.comments
            project_comments = project_comments + "***" + comment
            project.comments = project_comments
        else:
            project.comments = comment
        project.nomination_form_hdc_verified = False
        project.nomination_form_submitted = False
        project.reset_appointed_assessors()
        project.save()
        t = threading.Thread(target=send_reject_email, args=(project.get_supervisor().email,))
        t.start()
        messages.success(request, "Project returned to supervisor successfully")
        return redirect(url)
    else:
        messages.error(request, "Comment cannot be empty")
        return redirect(url)