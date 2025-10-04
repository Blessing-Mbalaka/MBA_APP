from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from mbamain.models import Invite
from mbamain.utils.shortcuts import require_scholar, require_examiner
from django.contrib import messages

@require_scholar
def accept_invite(request, invite_id):
    if request.method != "POST":
        return HttpResponseNotFound("Invalid request method")
    invite = get_object_or_404(Invite, id=invite_id, user=request.user, )
    invite.response = True
    invite.read = True
    invite.save()
    messages.success(request, "Invite accepted successfully")
    return redirect("mba_main:index_scholar")

@require_scholar
def decline_invite(request, invite_id):
    if request.method != "POST":
        return HttpResponseNotFound("Invalid request method")
    invite = get_object_or_404(Invite, id=invite_id, user=request.user, )
    invite.response = False
    invite.read = True
    invite.save()
    messages.success(request, "Invite declined successfully")
    return redirect("mba_main:index_scholar")

@require_scholar
def invites(request):
    invites = request.user.user_invites.filter(read=False).order_by('-created_at')
    return render(request, "mbamain/scholar/invites.html", {"invites": invites})


#examiner's invites 
@require_examiner
def examiner_invites(request):
    invites = request.user.user_invites.filter(read=False).order_by('-created_at')
    return render(request, "mbamain/examiner/invites.html", {"invites": invites})

@require_examiner
def examiner_accept_invite(request, invite_id):
    if request.method != "POST":
        return HttpResponseNotFound("Invalid request method")
    invite = get_object_or_404(Invite, id=invite_id, user=request.user, )
    invite.response = True
    invite.read = True
    invite.response = False
    email = invite.user.email
    project = invite.project
    email_1 = project.get_assessor_1().email if  project.get_assessor_1() else ''
    email_2 = project.get_assessor_2().email if  project.get_assessor_2() else '' 
    email_3 = project.get_assessor_3().email if  project.get_assessor_3() else ''
    print(email, email_1, email_2, email_3)
    if email == email_1:
        project.assessor_1_responded = True
        project.assessor_1_response = True
    elif email == email_2:
        project.assessor_2_responded = True
        project.assessor_2_response = True
    elif email == email_3:
        project.assessor_3_responded = True
        project.assessor_3_response = True
    project.save()
  
    invite.save()
    messages.success(request, "Invite accepted successfully")
    return redirect("mba_main:examiner_invites")

@require_examiner
def examiner_decline_invite(request, invite_id):
    if request.method != "POST":
        return HttpResponseNotFound("Invalid request method")
    invite = get_object_or_404(Invite, id=invite_id, user=request.user, )
    invite.response = False
    invite.read = True
    email = invite.user.email
    project = invite.project
    email_1 = project.get_assessor_1().email
    email_2 = project.get_assessor_2().email
    email_3 = project.get_assessor_3().email

    if email == email_1:
        project.assessor_1_responded = True
        project.assessor_1_response = False
    elif email == email_2:
        project.assessor_2_responded = True
        project.assessor_2_response = False
    elif email == email_3:
        project.assessor_3_responded = True
        project.assessor_3_response = False
    project.save()
    invite.save()
    messages.success(request, "Invite declined successfully")
    return redirect("mba_main:examiner_invites")