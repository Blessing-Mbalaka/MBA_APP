from django.db import models 

class NominationForm(models.Model):
    project = models.OneToOneField('mbamain.Project', related_name="nomination_form", on_delete=models.CASCADE, null=False, blank=False)

    co_supervisor_full_names = models.TextField(null=True, blank=True)
    co_supervisor_department = models.TextField(null=True, blank=True)
    co_supervisor_phone = models.TextField(null=True, blank=True)
    co_supervisor_email = models.TextField(null=True, blank=True)
    degree = models.TextField(null=True, blank=True)
    qualification = models.TextField(null=True, blank=True)
    
    supervisor_signed = models.BooleanField(null=True, default=False)
    supervisor_sign_date = models.DateField(null=True, blank=True, auto_now=True)
    

    