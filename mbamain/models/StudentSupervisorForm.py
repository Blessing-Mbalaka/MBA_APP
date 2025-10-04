from django.db import models

class StudentSupervisorForm(models.Model):
    project = models.OneToOneField('mbamain.Project', related_name="sp_form", on_delete=models.CASCADE)
    initials_student = models.CharField(null=True, max_length=100)
    initials_supervisor = models.CharField(null=True, max_length=100)
    date_signed_student = models.DateField(auto_now=True)
    supervisors_signed_date = models.DateField(auto_now=True)
    supervisor_signed = models.BooleanField(null=True, default=False)
    student_signed = models.BooleanField(null=True, default=False)
    student_address = models.TextField(null=True)
    supervisor_department = models.TextField(null=True)
    co_supervisor_department = models.TextField(null=True)
    co_supervisor_full_names = models.TextField(null=True)
    co_supervisor_initials = models.TextField(null=True)
    co_supervisor_surname = models.TextField(null=True)
    student_signed = models.BooleanField(default=False)
    supervisor_signed = models.BooleanField(default=False)
    
  
    def __str__(self):
        return f"This is a JBS5 form"