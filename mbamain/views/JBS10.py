from mbamain.utils import require_student, require_auth, require_scholar, clean_title
from mbamain.models import Project, JBS10
from django.shortcuts import get_object_or_404 ,render, redirect
from django.http import HttpResponseForbidden, Http404
from django.utils import timezone
from django.contrib import messages


def form(request, project_id):
    project = get_object_or_404(Project,pk=project_id)
    return render(request, "mbamain/academicForms/JBS10.html", {"project": project, "student": project.student})


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
        
        proposed_title = request.POST.get("proposed_title")
        previous_title = request.POST.get("previous_title")

        proposed_title = clean_title(proposed_title)
        previous_title = clean_title(previous_title)

        if proposed_title is None or (previous_title is None):
            messages.error(request, "title must be  at most 15 words.")
            return redirect("mba_main:jbs10_form", project_id=project_id)
        
        jbs10_instance, created = JBS10.objects.get_or_create(project=project)
        fields = [
            # Section A: Student Information
            "is_uj_staff",
            "ethical_clearance_number",
            "capstone_project",

            # Section B: Title Registration/Amendment
            "proposed_title",
            "is_4ir_research",
            "previous_title",

            # Section C: Supervisor Registration/Amendment
            "supervisor_name",
            "supervisor_staff_number",

            "cosupervisor1_name",
            "cosupervisor1_staff_number",

            "cosupervisor2_name",
            "cosupervisor2_staff_number",

            "previous_supervisor_name",
            "previous_supervisor_staff_number",

            "previous_cosupervisor_name",
            "previous_cosupervisor_stuff_number",

            # Section D: Assessor Nomination/Amendment
            "internal_assessor",

            "external_assessor1_name",
            "external_assessor1_staff_number",
            "external_assessor1_affiliation",
            "external_assessor1_qualification",
            "external_assessor1_email",

            "external_assessor2_name",
            "external_assessor2_staff_number",
            "external_assessor2_affiliation",
            "external_assessor2_qualification",
            "external_assessor2_email",

            "external_assessor3_name",
            "external_assessor3_staff_number",
            "external_assessor3_affiliation",
            "external_assessor3_qualification",
            "external_assessor3_email",

            # D3 Amendment of internal assessor
            "previous_assessor_name",
            "previous_assessor_qualification",
            "previous_assessor_staff_number",

            # D4 Amendment of external assessor
            "previous_external_assessor1_name",
            "previous_external_assessor1_staff_number",
            "previous_external_assessor1_affiliation",
            "previous_external_assessor1_qualification",
            "previous_external_assessor1_email",

            "previous_external_assessor2_name",
            "previous_external_assessor2_staff_number",
            "previous_external_assessor2_affiliation",
            "previous_external_assessor2_qualification",
            "previous_external_assessor2_email",

            "previous_external_assessor3_name",
            "previous_external_assessor3_staff_number",
            "previous_external_assessor3_affiliation",
            "previous_external_assessor3_qualification",
            "previous_external_assessor3_email",
        ]

        
        for field in fields:
            value = request.POST.get(field)
            if field == "proposed_title":
                setattr(jbs10_instance, field, proposed_title) 
                project.project_title = proposed_title
                project.save()
                continue
            if field == "previous_title":
                setattr(jbs10_instance, field, previous_title) 
                continue
            setattr(jbs10_instance, field, value)
        
        if request.user.is_scholar():
            if not jbs10_instance.supervisor_signed:
                jbs10_instance.supervisor_signed = timezone.now()
            jbs10_instance.supervisor_signed = True
        
        if request.user.is_student():
            if not jbs10_instance.student_signed:
                jbs10_instance.student_signed = timezone.now()
            jbs10_instance.student_signed = True
        
        jbs10_instance.save()
        messages.success(request, "form signed successfully")
        return redirect("mba_main:jbs10_form", project_id=project_id)

    raise Http404()