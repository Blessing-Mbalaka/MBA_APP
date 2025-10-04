from mbamain.utils import require_student, require_auth, require_scholar
from mbamain.models import Project, JBS5
from django.shortcuts import get_object_or_404 ,render, redirect
from django.http import HttpResponseForbidden, Http404, HttpResponseNotFound
from django.utils import timezone
from django.contrib import messages


def form(request, project_id):
    project = get_object_or_404(Project,pk=project_id)
    return render(request, "mbamain/academicForms/JBS5.html", {"project": project, "student": project.student})


@require_auth
def signform(request, project_id):
    if request.method == "POST":
        # Handle form submission logic here
        project = get_object_or_404(Project, pk=project_id)
        if not project.primary_supervisor:
            messages.error(request, "This project does not have a primary supervisor assigned yet. Please contact the admin to assign a primary supervisor.")
            return redirect('mba_main:jbs5_form', project_id=project.id)
        user = request.user
        if (user.is_student() and not user.id == project.student.id) or (user.is_scholar() and not user.id == project.primary_supervisor):
            return HttpResponseForbidden()
        study_type = request.POST.get("study_type")
        ir = request.POST.get('4ir')
        title = request.POST.get("title")
        initials = request.POST.get("initials")
        qualification = request.POST.get("qualification")
        reg_date = request.POST.get("registration_date", timezone.now().date())
        form, created = JBS5.objects.get_or_create(project=project)
        research_specific = request.POST.get("research_specific")
        secondary_focus = request.POST.get("secondary_focus")

        
    
        if user.is_student() or user.is_scholar():
            project.project_title = title
            project.save() # update the project title
            form.title = title
            project.project_title = title
            project.save() # update the project title
            form.qualification = qualification
            form.registration_date = reg_date
            form.study_type = study_type
            form.ir = ir
            form.initials = initials
            form.research_specific = research_specific
            form.secondary_focus  = secondary_focus

            form.previous_title = request.POST.get("previous_title")
            form.proposed_amendment_title = request.POST.get("proposed_amendment_title")
            form.proposed_supervisor = request.POST.get("proposed_supervisor")
            form.previously_approved_supervisor = request.POST.get("previously_approved_supervisor")
            form.amended_supervisor = request.POST.get("amended_supervisor")
            form.proposed_co_supervisor = request.POST.get("proposed_co_supervisor")
            form.previously_approved_co_supervisor = request.POST.get("previously_approved_co_supervisor")
            form.amended_co_supervisor = request.POST.get("amended_co_supervisor")
            

            if user.is_scholar():
                form.supervisors_signed_date = timezone.now()
                form.supervisor_signed = True
                
            if user.is_student():
                form.student_signed_date = timezone.now()
                form.student_signed= True
            
            form.save()
            messages.success(request, "form signed successfully")
            return redirect('mba_main:jbs5_form', project_id=project.id)
        return HttpResponseForbidden()
    return HttpResponseNotFound()

@require_auth
def submit_jbs5_form(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        if project.project_status == Project.ProjectStatus.JBS5_submitted:
            messages.error(request, "JBS5 form has already been submitted for this project.")
            print("JBS5 form has already been submitted for this project.")
            return redirect('mba_main:manage_project', id=project.id)
        #check if supervisor submitting 
        if not request.user.is_scholar() or request.user.id != project.primary_supervisor:
            return HttpResponseForbidden("You do not have permission to submit this form.")
        if not project.can_submit_jbs5():
            messages.error(request, "Both the student and supervisor must sign the form before submission.")
            return redirect('mba_main:jbs5_form', project_id=project.id)
        project.project_status = Project.ProjectStatus.JBS5_submitted
        project.save()
        messages.success(request, "JBS5 form submitted successfully.")
        return redirect('mba_main:manage_project', id=project.id)
    return HttpResponseNotFound()