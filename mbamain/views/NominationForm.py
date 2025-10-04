from mbamain.utils import require_student, require_auth, require_scholar
from mbamain.models import Project, JBS5, NominationForm
from django.shortcuts import get_object_or_404 ,render, redirect
from django.http import HttpResponseForbidden, Http404, HttpResponseNotFound
from django.utils import timezone
from django.contrib import messages

# @require_auth
def form(request, project_id):
    project = get_object_or_404(Project,pk=project_id)
    
    return render(request, "mbamain/academicForms/NominationForm.html", {"project": project, "student": project.student})


@require_auth
def signform(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=project_id)
        user = request.user
        if (user.is_student()) or (user.is_scholar() and not user.id == project.primary_supervisor):
            return HttpResponseForbidden()
         
     
        form,_ = NominationForm.objects.get_or_create(project=project)
        co_supervisor_full_names = request.POST.get("co_supervisor_full_names")
        co_supervisor_department = request.POST.get("co_supervisor_department")
        co_supervisor_phone = request.POST.get("co_supervisor_phone")
        co_supervisor_email = request.POST.get("co_supervisor_email")
        form.co_supervisor_email = co_supervisor_email
        form.co_supervisor_phone = co_supervisor_phone
        form.co_supervisor_department= co_supervisor_department
        form.co_supervisor_full_names = co_supervisor_full_names
        form.qualification = request.POST.get("qualification")
        form.degree = request.POST.get("degree")
        form.supervisor_signed = True
        form.supervisor_sig_date = timezone.now()
        form.save()
        messages.success(request, "Nomination form signed successfully.")
        return redirect('mba_main:nominaton_form', project_id=project.id)
        
    return HttpResponseNotFound()


@require_auth
def submit_nomination_form(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        #check if supervisor submitting 
        if not request.user.is_scholar() or request.user.id != project.primary_supervisor:
            return HttpResponseForbidden("You do not have permission to submit this form.")
        
        if not project.cansubmit_nomination():
            messages.error(request, "You cannot submit this nomination form. Please ensure that the form is signed by the supervisor.")
            return redirect("mba_main:manage_project", id=project.id)
        print("Can sumbit nomination")
        print(project.cansubmit_nomination)
        project.nomination_form_submitted = True
        project.save()
        messages.success(request, "Nomination form submitted successfully.222")
        return redirect('mba_main:manage_project', id=project.id)
    return HttpResponseNotFound()