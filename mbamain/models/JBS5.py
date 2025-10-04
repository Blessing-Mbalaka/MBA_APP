from django.db import models

class JBS5(models.Model):
    project = models.OneToOneField('mbamain.Project', related_name="jbs5_form", on_delete=models.CASCADE)
    student_signature = models.ForeignKey("mbamain.Signature", related_name="jbs5_forms", null=True, blank=False, on_delete=models.DO_NOTHING)
    initials = models.CharField(null=True)
    superivosr_signed = models.BooleanField(null=True, default=False)
    date_signed_student = models.DateField(auto_now=True)
    supervisors_signed_date = models.DateField(auto_now=True)
    study_type = models.TextField(null=True)
    ir = models.TextField(null=True, blank=True)
    qualification = models.TextField(null=True)
    title = models.TextField(null=True)
    research_specific = models.BooleanField(null=True)
    secondary_focus = models.BooleanField(null=True)
    registration_date = models.DateField(null=True)
    co_supervisor_surname = models.TextField(null=True, blank=True)
    co_supervisor_initials = models.TextField(null=True, blank=True)
    co_supervisor_department = models.TextField(null=True, blank=True)
    student_signed = models.BooleanField(default=False)
    supervisor_signed = models.BooleanField(default=False)

    proposed_supervisor = models.TextField(null=True, default='')
    proposed_co_supervisor = models.TextField(null=True, default='')
    previously_approved_supervisor = models.TextField(null=True, default='')
    amended_supervisor = models.TextField(null=True, default='')
    previously_approved_co_supervisor = models.TextField(null=True, default='')
    amended_co_supervisor = models.TextField(null=True, default='')
    previous_title = models.TextField(null=True, default='')
    proposed_amendment_title = models.TextField(null=True, default='')

    def __str__(self):
        return f"This is a JBS5 form"