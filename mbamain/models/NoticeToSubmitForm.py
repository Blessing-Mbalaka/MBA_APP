from django.db import models

class NoticeToSubmitForm(models.Model):
    project = models.OneToOneField('mbamain.Project', related_name="notice_form", on_delete=models.CASCADE)
    student_signature = models.ForeignKey("mbamain.Signature", related_name="notice_forms", null=True, blank=False, on_delete=models.DO_NOTHING)
    primary_supervisor_signature =  models.ForeignKey("mbamain.Signature", related_name="primary_notice_forms",null=True, blank=False, on_delete=models.DO_NOTHING)
    secondary_supervisor_signature =  models.ForeignKey("mbamain.Signature", related_name="secondary_notice_forms",null=True, blank=False, on_delete=models.DO_NOTHING)
    hod_signature =  models.ForeignKey("mbamain.Signature", related_name='hod_notice_forms', null=True, blank=False, on_delete=models.DO_NOTHING)
    dos_signature =  models.ForeignKey("mbamain.Signature", null=True, related_name="dos_notice_forms", blank=False, on_delete=models.DO_NOTHING)

    date_signed_student = models.DateField(auto_now=True)
    auth_student = models.CharField(max_length=100, null=True, blank=True)  
    supervisors_comment = models.TextField(null=True, blank=True)
    supervisor_agree = models.BooleanField(null=True, default=False)
    supervisors_signed_date = models.DateField(auto_now=True)
    approved_hdc = models.BooleanField(null=True, default=False)
    title_approved_hdc = models.BooleanField(null=True, default=False)
    ethicals = models.TextField( null=True, blank=True)  
    nominated_examinners = models.BooleanField(null=True, default=False)
    co_supervisor_details = models.TextField(null=True)
    student_signed = models.BooleanField(default=False)
    supervisor_signed = models.BooleanField(default=False)



    def __str__(self):
        return f"This is a notice form"