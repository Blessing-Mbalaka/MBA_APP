from mbamain.utils import require_student, require_auth, require_scholar
from mbamain.models import Project, StudentSupervisorForm
from django.shortcuts import get_object_or_404 ,render,redirect
from django.http import HttpResponseForbidden, Http404
from django.utils import timezone
from django.contrib import messages



# @require_auth
def form(request, project_id):
    project = get_object_or_404(Project,pk=project_id)
    return render(request, "mbamain/academicForms/studentSupervisorForm.html", {"project": project, "student": project.student})


@require_auth
def signform(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=project_id)
        if not project.primary_supervisor:
            messages.error(request, "This project does not have a primary supervisor assigned yet. Please contact the admin to assign a primary supervisor.")
            return redirect('mba_main:student_supervisor_form', project_id=project.id)
        user = request.user
        if (user.is_student() and not user.id == project.student.id) or (user.is_scholar() and not user.id == project.primary_supervisor):
            return HttpResponseForbidden()
        
        initials_student = request.POST.get("student_initials")
        initials_supervisor = request.POST.get("supervisor_initials")
        degree = request.POST.get("degree")
        student_address = request.POST.get("student_address")
        supervisor_department = request.POST.get("supervisor_department")
        co_supervisor_department = request.POST.get("co_supervisor_department")
        co_supervisor_surname = request.POST.get("co_supervisor_surname")
        co_supervisor_initials = request.POST.get("co_supervisor_initials")
        co_supervisor_full_names = request.POST.get("co_supervisor_full_names")
         
        form, created = StudentSupervisorForm.objects.get_or_create(project=project)

        if user.is_student() or user.is_scholar():
            form.initials_student = initials_student
            form.initials_supervisor = initials_supervisor
            form.co_supervisor_full_names = co_supervisor_full_names
            form.co_supervisor_department = co_supervisor_department
            form.co_supervisor_surname = co_supervisor_surname
            form.co_supervisor_initials = co_supervisor_initials
            form.student_address = student_address
            form.supervisor_department = supervisor_department
            if user.is_scholar():
                form.supervisors_signed_date = timezone.now()
                form.supervisor_signed = True
            
            if user.is_student():
                form.date_signed_student = timezone.now()
                form.student_signed = True
            
            form.save()
            messages.success(request, "form signed successfully")
            return redirect('mba_main:student_supervisor_form', project_id=project.id)
        
        return HttpResponseForbidden()
    