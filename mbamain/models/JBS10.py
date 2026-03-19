from django.db import models

class JBS10(models.Model):
    CAPSTONE_CHOICES = [
        ('limited', 'Limited scope dissertation'),
        ('minor', 'Minor dissertation'),
        ('dissertation', 'Dissertation'),
        ('thesis', 'Thesis'),
        ('monograph', 'Monograph'),
        ('article', 'By article'),
    ]
    project = models.OneToOneField('mbamain.Project', related_name="jbs10_form", on_delete=models.CASCADE)
    # Section A: Student Information
    is_uj_staff = models.BooleanField(null=True,default=False)
    ethical_clearance_number = models.TextField(null=True, max_length=50, blank=True)
    capstone_project = models.TextField(null=True, max_length=20, choices=CAPSTONE_CHOICES)
    
    # Section B: Title Registration/Amendment
    proposed_title = models.TextField(null=True)
    is_4ir_research = models.BooleanField(null=True,default=False)
    previous_title = models.TextField(null=True, blank=True)  # For amendments
    
    # Section C: Supervisor Registration/Amendment
    #C1
    supervisor_name = models.TextField(null=True, max_length=200)
    supervisor_staff_number = models.TextField(null=True, max_length=20)

    cosupervisor1_name = models.TextField(null=True, max_length=200, blank=True, default='')
    cosupervisor1_staff_number = models.TextField(null=True, max_length=20, blank=True)

    cosupervisor2_name = models.TextField(null=True, max_length=200, blank=True, default='')
    cosupervisor2_staff_number = models.TextField(null=True, max_length=20, blank=True)

    # c2
    previous_supervisor_name = models.TextField(null=True, max_length=200, blank=True, default='')  # For amendments
    previous_supervisor_staff_number = models.TextField(null=True, max_length=200, blank=True, default='')  # For amendments

    previous_cosupervisor_name = models.TextField(null=True, max_length=200, blank=True, default='')  # For amendments
    previous_cosupervisor_stuff_number = models.TextField(null=True, max_length=200, blank=True, default='')  # For amendments
    
    # Section D: Assessor Nomination/Amendment
    #D1
    internal_assessor = models.TextField(null=True, max_length=200, blank=True, default='')
    #D2
    external_assessor1_name = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor1_staff_number = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor1_affiliation = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor1_qualification = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor1_email = models.EmailField(null=True,blank=True, default='')
    external_assessor2_name = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor2_staff_number = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor2_affiliation = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor2_qualification = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor2_email = models.EmailField(null=True,blank=True, default='')
    
    external_assessor3_name = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor3_staff_number = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor3_affiliation = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor3_qualification = models.TextField(null=True, max_length=200, blank=True, default='')
    external_assessor3_email = models.EmailField(null=True,blank=True, default='')


    #D3 Ammendment of internal assessor
    previous_assessor_name = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_assessor_qualification = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_assessor_staff_number = models.TextField(null=True, max_length=200, blank=True, default='')

    #D4 Ammendment of external assessor
    previous_external_assessor1_name = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor1_staff_number = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor1_affiliation = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor1_qualification = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor1_email = models.EmailField(null=True,blank=True, default='')
    
    previous_external_assessor2_name = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor2_staff_number = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor2_affiliation = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor2_qualification = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor2_email = models.EmailField(null=True,blank=True, default='')
    
    previous_external_assessor3_name = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor3_staff_number = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor3_affiliation = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor3_qualification = models.TextField(null=True, max_length=200, blank=True, default='')
    previous_external_assessor3_email = models.EmailField(null=True,blank=True, default='')


    # Signatures
    supervisor_signed = models.TextField(null=True, max_length=100, blank=True)
    supervisor_signed_date = models.DateField(null=True, blank=True)
    

    # Signatures
    student_signed = models.TextField(null=True, max_length=100, blank=True)
    student_signed_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.surname} - {self.proposed_title}"