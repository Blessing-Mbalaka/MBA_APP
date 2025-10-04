from django.shortcuts import redirect, render
from mbaAdmin.utils import is_admin
from mbamain.models import AUser, ExamminerProfile

@is_admin
def index(request):
    number_of_students = AUser.objects.filter(user_type=AUser.UserType.STUDENT).count()
    number_of_supervisors = AUser.objects.filter(user_type=AUser.UserType.SCHOLAR).count()
    examiners_no = ExamminerProfile.objects.count()
    return render(request, "mbaAdmin/activities.html", {
        "students_no": number_of_students,
        "supervisors_no": number_of_supervisors,
        "examiners_no": examiners_no
    })
