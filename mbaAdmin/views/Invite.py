from django.shortcuts import redirect, render, get_object_or_404
from mbaAdmin.utils import is_admin, send_supervisor_invite, send_appointed, supervisor_allocated, send_assessor_invite_email
from mbamain.models import Invite, Project, AUser
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseServerError
import threading
@is_admin
def send_invite(request):
    if request.method == "POST":
        supervisors_ids = request.POST.getlist("supervisors")
        project_id = request.POST.get("project_id")
        student_id = request.POST.get("student_id")
        
        try:
            project  = Project.objects.get(id=project_id)
            if project.primary_supervisor:
                messages.success(request, "The supervisor has already been appointed")
                return redirect("mba_admin:manage_student", student_id) 
            for supervisor_id in supervisors_ids:
                supervisor = AUser.objects.get(id=supervisor_id)
                _,created = Invite.objects.get_or_create(user=supervisor, project=project)
                t = threading.Thread(target=send_supervisor_invite, args=(supervisor.email, project))
                t.start()
            messages.success(request, "Invites sent successfully")
                 
        except Exception as e:
            print(e)
            messages.error(request, "Invite was not sent")
        return redirect("mba_admin:manage_student", student_id) 
    

@is_admin
def send_assessor_invite(request):
     project_id = request.GET.get('project_id')
     assessor_no = request.GET.get('n')
     project = get_object_or_404(Project, id=project_id)
     if assessor_no not in ['1','2','3']:
            return HttpResponseNotFound("Invalid assessor number")
     if assessor_no == '1':
         if not project.assessor_1_approved:
             messages.error(request, "Assessor 1 has not been approved yet")
             return redirect("mba_admin:nomination_submitted")
         assessor = project.get_assessor_1().user
         _,created = Invite.objects.get_or_create(user=assessor, project=project)
         project.assessor_1_invite_sent = True
         t = threading.Thread(target=send_assessor_invite_email, args=(assessor.email, project))
         t.start()
     elif assessor_no == '2':
         if not project.assessor_2_approved:
                messages.error(request, "Assessor 2 has not been approved yet")
                return redirect("mba_admin:nomination_submitted")
         assessor = project.get_assessor_2().user
         _,created = Invite.objects.get_or_create(user=assessor, project=project)
         project.assessor_2_invite_sent = True
         t = threading.Thread(target=send_assessor_invite_email, args=(assessor.email, project))
         t.start()
     elif assessor_no == '3':
            if not project.assessor_3_approved:
                    messages.error(request, "Assessor 3 has not been approved yet")
                    return redirect("mba_admin:nomination_submitted")
            assessor = project.get_assessor_3().user
            _,created = Invite.objects.get_or_create(user=assessor, project=project)
            project.assessor_3_invite_sent = True
            t = threading.Thread(target=send_assessor_invite_email, args=(assessor.email, project))
            t.start()
     project.save()
     messages.success(request, "Invite sent successfully")
     return redirect("mba_admin:nomination_submitted")
     
@is_admin
def appoint_supervisor(request):
    if request.method != "POST":
        return HttpResponseNotFound("Method not allowed")
    supervisor_id = request.POST.get("supervisor_id")
    project_id = request.POST.get("project_id")
    try:
        project = Project.objects.get(id=project_id)
        supervisor = AUser.objects.get(id=supervisor_id)
        supervisor.supervisor_profile.students = supervisor.supervisor_profile.students + 1 
        supervisor.supervisor_profile.save()
        project.primary_supervisor = supervisor.id
        t2 = threading.Thread(target=supervisor_allocated, args=(project.project_title,project.student.email , project))
        t = threading.Thread(target=send_appointed, args=(project.project_title, supervisor.email))
        t2.start()  # Start the thread to send the student email
        t.start()  # Start the thread to send the appointment email
        #retract all the invites for the project
        Invite.objects.filter(project=project).delete()
        project.save()
        messages.success(request, "Supervisor appointed successfully")
        return redirect("mba_admin:manage_student", project.student.id)
    except Exception as e:
        print(e)
        return HttpResponseServerError()
   