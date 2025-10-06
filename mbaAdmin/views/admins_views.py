from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.http import HttpResponseForbidden, HttpResponseNotFound
from mbaAdmin.utils import is_admin, project_status_changed_email, is_valid_email, send_project_to_assessor
from mbamain.models import Project, AUser
from django.contrib import messages
import threading

@is_admin
def manage_admins(request):
    return render(request, "mbaAdmin/admins.html")

@is_admin
def approve_title(request):
    page = request.GET.get("page", 0)
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0

    student_no = request.GET.get("student_no", '')
  
    url = reverse("mba_admin:titles_submitted") +  f"?page={page}&student_no={student_no}"
    if request.method == "POST":
     project_id = request.POST.get("project_id")
     project = get_object_or_404(Project, pk=project_id)
     project.project_status = Project.ProjectStatus.JBS5_Admin_approved
     messages.success(request, "Project title approved successfully.")
     t = threading.Thread(target=project_status_changed_email, args=(project.student.email, "Your project title has been approved by  Admin. And is sent for HDC approval"))
     t.start()
     t = threading.Thread(target=project_status_changed_email, args=(project.get_supervisor().email, f"The project title for student {project.student.email} has been approved by Admin. And is sent for HDC approval"))
     t.start()
     project.save()
     return redirect(url)
     
    return HttpResponseNotFound()

@is_admin
def decline_title(request):
   if request.method == "POST":
      page = request.GET.get("page", 0)
      try:
        page = int(page)
        if page < 0:
            page = 0
      except ValueError:
        page = 0

      student_no = request.GET.get("student_no", '')
      url = reverse("mba_admin:titles_submitted") +  f"?page={page}&student_no={student_no}"
      project_id = request.POST.get("project_id")
      project = get_object_or_404(Project, pk=project_id)
      comment = request.POST.get("comment")
      # make sure comment is not empty
      if not comment:
            messages.error(request, "Please provide a comment for declining the title.")
            return redirect(url)
      if project.comments:
            project.comments += "***" + comment
      else:
            project.comments = comment
      project.project_status = Project.ProjectStatus.JBS5_Admin_declined
      t = threading.Thread(target=project_status_changed_email, args=(project.student.email, "Your project title has been declined by  Admin. Please check the comments and resubmit."))
      t.start()
      t = threading.Thread(target=project_status_changed_email, args=(project.get_supervisor().email, f"The project title for student {project.student.email} has been declined by Admin. Please check the comments and resubmit."))
      t.start()
      project.save() 
      messages.success(request, "Project title declined successfully.")
      return redirect(url)   
   return HttpResponseNotFound()


@is_admin
def decline_intent(request):
   if request.method == "POST":
      page = request.GET.get("page", 0)
      try:
        page = int(page)
        if page < 0:
            page = 0
      except ValueError:
        page = 0

      student_no = request.GET.get("student_no", '')
      url = reverse("mba_admin:intent_submitted") +  f"?page={page}&student_no={student_no}"
      project_id = request.POST.get("project_id")
      project = get_object_or_404(Project, pk=project_id)
      comment = request.POST.get("comment")
      # make sure comment is not empty
      if not comment:
            messages.error(request, "Please provide a comment for declining the intent.")
            return redirect(url)
      if project.comments:
            project.comments += "***" + comment
      else:
            project.comments = comment
      project.intent_form_submitted = False
      t = threading.Thread(target=project_status_changed_email, args=(project.student.email, "Your project intent form has been declined by  Admin. Please check the comments and resubmit."))
      t.start()
      t = threading.Thread(target=project_status_changed_email, args=(project.get_supervisor().email, f"The project intent form for student {project.student.email} has been declined by Admin. Please check the comments and resubmit."))
      t.start()
      project.save() 
      messages.success(request, "Project intent declined successfully.")
      return redirect(url)   
   return HttpResponseNotFound()

@is_admin
def approve_notice_form(request):
    if request.method == "POST":
     project_id = request.POST.get("project_id")
     project = get_object_or_404(Project, pk=project_id)
     project.project_status = Project.ProjectStatus.Notice_Admin_approved
     messages.success(request, "Notice form approved successfully.")
     t = threading.Thread(target=project_status_changed_email, args=(project.student.email, "Your project notice form has been approved by  Admin."))
     t.start()
     t = threading.Thread(target=project_status_changed_email, args=(project.get_supervisor().email, f"The project notice form for student {project.student.email} has been approved by Admin."))
     t.start()
     project.save()
     return redirect('mba_admin:titles_submitted')
    return HttpResponseNotFound()

@is_admin
def decline_notice_form(request):
   if request.method == "POST":
      project_id = request.POST.get("project_id")
      project = get_object_or_404(Project, pk=project_id)
      comment = request.POST.get("comment")
      # make sure comment is not empty
      if not comment:
            messages.error(request, "Please provide a comment for declining the notice form.")
            return redirect('mba_admin:titles_submitted')
      if project.comments:
            project.comments += "***" + comment
      else:
            project.comments = comment
      project.project_status = Project.ProjectStatus.Notice_Admin_declined
      project.save()
      t = threading.Thread(target=project_status_changed_email, args=(project.student.email, "Your project notice form has been declined by  Admin. Please check the comments and resubmit."))
      t.start()
      t = threading.Thread(target=project_status_changed_email, args=(project.get_supervisor().email, f"The project notice form for student {project.student.email} has been declined by Admin. Please check the comments and resubmit."))
      t.start() 
      messages.success(request, "Notice form declined successfully.")
      return redirect('mba_admin:titles_submitted')   
   return HttpResponseNotFound()



@is_admin
def activate_student(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(AUser, pk=user_id)
        if user.is_admin():
            return HttpResponseForbidden("You cannot deactivate another admin.")
        user.set_active(True)
        user.save()
        user = get_object_or_404(AUser, pk=user_id)
        messages.success(request, f"User {user.is_active} activated successfully.")
        return redirect(reverse("mba_admin:students"))
    return HttpResponseNotFound("Page not found.")


@is_admin
def suspend_student(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(AUser, pk=user_id)
        if user.is_admin():
            return HttpResponseForbidden("You cannot deactivate another admin.")
        user.set_active(False)
        user.save()
        messages.success(request, f"User {user.email} suspended successfully.")
        return redirect(reverse("mba_admin:students"))
    return HttpResponseNotFound("Page not found.")

@is_admin
def activate_examiner(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(AUser, pk=user_id)
        if user.is_admin():
            return HttpResponseForbidden("You cannot deactivate another admin.")
        user.set_active(True)
        user.save()
        messages.success(request, f"User {user.email} activated successfully.")
        return redirect(reverse("mba_admin:examiners"))
    return HttpResponseNotFound("Page not found.")


@is_admin
def suspend_examiner(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(AUser, pk=user_id)
        if user.is_admin():
            return HttpResponseForbidden("You cannot deactivate another admin.")
        user.set_active(False)
        user.save()
        messages.success(request, f"User {user.email} suspended successfully.")
        return redirect(reverse("mba_admin:examiners"))
    return HttpResponseNotFound("Page not found.")

@is_admin
def activate_supervisor(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(AUser, pk=user_id)
        if user.is_admin():
            return HttpResponseForbidden("You cannot deactivate another admin.")
        user.set_active(True)
        user.save()
        messages.success(request, f"User {user.email} activated successfully.")
        return redirect(reverse("mba_admin:supervisors"))
    return HttpResponseNotFound("Page not found.")


@is_admin
def suspend_supervisor(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(AUser, pk=user_id)
        if user.is_admin():
            return HttpResponseForbidden("You cannot deactivate another admin.")
        user.set_active(False)
        user.save()
        messages.success(request, f"User {user.email} suspended successfully.")
        return redirect(reverse("mba_admin:supervisors"))
    return HttpResponseNotFound("Page not found.")


@is_admin
def upload_project(request, project_id):
    if request.method != "POST":
        return HttpResponseNotFound("Method not allowed")
    project = get_object_or_404(Project, pk=project_id)
   
    try:
        if 'project_file' not in request.FILES:
            messages.error(request, "No file uploaded.")
            return redirect(reverse("mba_admin:nomination_submitted"))
        project_file = request.FILES['project_file']
        #send this file to assessor via email 
        assessor = request.GET.get('assessor')
        print(assessor)
        if not assessor in ['1','2']:
            messages.error(request, "Invalid assessor number.")
            return redirect(reverse("mba_admin:nomination_submitted"))
        if assessor == '1':
            email = project.assessor_1_email
            if is_valid_email(email):
                send_project_to_assessor(email,project.student.student_profile.student_no, project_file)
            else:
                messages.error(request, "Assessor 1 email is not valid.")
                return redirect(reverse("mba_admin:nomination_submitted"))
            
    
        if assessor == '2':
            email = project.assessor_2_email
            if is_valid_email(email):
                send_project_to_assessor(email,project.student.student_profile.student_no, project_file)
            else:
                messages.error(request, "Assessor 2 email is not valid.")
                return redirect(reverse("mba_admin:nomination_submitted"))
            
    
        messages.success(request, "Project file uploaded successfully.")
    except Exception as e:
        print(e)
        messages.error(request, "Project file was not uploaded.")
    return redirect(reverse("mba_admin:nomination_submitted",))



