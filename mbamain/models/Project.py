
from django.db import models
from mbamain.models import AUser, ExamminerProfile

class Project(models.Model):
    class ProjectStatus(models.IntegerChoices):
        CREATED = 0, 'Created'
        HDC_SUBMITTED = 1, "Subtmited to ADMIN"
        HDC_APPROVED =2, "Approved for HDC by ADMIN"
        HDC_DECLINED =3, "Rejected by  ADMIN"
        ADMIN_APPROVED =4, "Approved by ADMIN"
        ADMIN_DECLINED =5, "Rejected by  ADMIN"
        GRADUATED =6, "project has completed"
        HDC_VERIFIED =7, "Verified by HDC"

        JBS5_submitted = 8, "JBS5 form submitted"
        JBS5_Admin_declined = 9, "JBS5 declined by admin "
        JBS5_Admin_approved = 10, "JBS5 approved by admin"
        JBS5_HDC_declined = 11, "JBS5 declined by HDC "
        JBS5_HDC_approved = 12, "JBS5 approved by HDC"

        Notice_submitted = 13, "Notice form submitted"
        Notice_Admin_declined = 14, "Notice form declined by admin "
        Notice_Admin_approved = 15, "Notice form approved by admin"
        Notice_HDC_declined = 16, "Notice form declined by HDC "
        Notice_HDC_approved = 17, "Notice form approved by HDC"
        
        
    student = models.ForeignKey('mbamain.AUser', null=False, related_name="projects", blank=False, on_delete=models.DO_NOTHING)
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    project_start_date = models.DateField(auto_now_add=True) 
    created_date = models.DateTimeField(auto_now_add=True)
    ehical_clearance_number = models.IntegerField(null=True, blank=True,default=0)
    qualification = models.CharField(max_length=100, null=True, blank=True,default=None) 
    project_status = models.IntegerField(choices=ProjectStatus.choices, default=ProjectStatus.CREATED)
    title_approved = models.BooleanField(null=True, default=False)
    nomination_form_approved = models.BooleanField(null=True, default=False)
    nomination_form_submitted = models.BooleanField(null=True, default=False)
    nomination_form_hdc_verified = models.BooleanField(null=True, default=False)

    intent_form_approved = models.BooleanField(null=True, default=False)
    intent_form_submitted = models.BooleanField(null=True, default=False)
    intent_form_hdc_verified = models.BooleanField(null=True, default=False)

    sdg_goal = models.TextField(null=True, default=' ')
    
    assessor_1_name = models.TextField(null=True, default=' ')
    assessor_1_email = models.TextField(null=True, default=' ')
    assessor_1_surname = models.TextField(null=True, default=' ')
    assessor_1_email_sent = models.BooleanField(null=True, default=False)

    assessor_2_name = models.TextField(null=True, default=' ')
    assessor_2_email = models.TextField(null=True, default=' ')
    assessor_2_surname = models.TextField(null=True, default=' ')
    assessor_2_email_sent = models.BooleanField(null=True, default=False)
    primary_supervisor = models.IntegerField(null=True)
    comments = models.TextField(null=True)
    hdc_comments = models.TextField(null=True)
    assessor_1_appointed = models.BooleanField(null=True, default=False)
    assessor_2_appointed = models.BooleanField(null=True, default=False)

    assessor_1_responded = models.BooleanField(null=True, default=False)
    assessor_2_responded = models.BooleanField(null=True, default=False)
    assessor_3_responded = models.BooleanField(null=True, default=False)
    assessor_1_response = models.BooleanField(null=True, default=False)
    assessor_1_invite_sent = models.BooleanField(null=True, default=False)
    assessor_2_response = models.BooleanField(null=True, default=False)
    assessor_2_invite_sent = models.BooleanField(null=True, default=False)
    assessor_3_response = models.BooleanField(null=True, default=False)
    assessor_3_invite_sent = models.BooleanField(null=True, default=False)
    assessor_1_approved = models.BooleanField(null=True, default=False)
    assessor_2_approved = models.BooleanField(null=True, default=False)
    assessor_3_approved = models.BooleanField(null=True, default=False)
    discipline  = models.TextField(null=False)
    assessor_1 = models.IntegerField(null=True, blank=True)
    assessor_2 = models.IntegerField(null=True, blank=True)
    assessor_3 = models.IntegerField(null=True, blank=True)

    def can_submit(self):
        return self.project_status == self.ProjectStatus.CREATED or self.project_status == self.ProjectStatus.HDC_DECLINED or self.project_status == self.ProjectStatus.ADMIN_DECLINED
    def get_comments(self):
        return ((self.comments or "").split("***") if self.comments else [])[::-1]
    def get_hdc_comments(self):
        return ((self.hdc_comments or "").split("***") if self.hdc_comments else [])[::-1] # reverse the comments to show the latest first 

    def get_supervisor(self):
        try:
            return AUser.objects.get(id=self.primary_supervisor)
        except:
            return None
    def get_assessor_1(self):
        
            return ExamminerProfile.objects.get(id=self.assessor_1)
    
    def reset_project(self):
        self.project_status = self.ProjectStatus.CREATED
        self.title_approved = False
        self.nomination_form_approved = False
        self.nomination_form_submitted = False
        self.nomination_form_hdc_verified = False
        self.intent_form_approved = False
        self.intent_form_submitted = False
        self.assessor_1_appointed = False
        self.assessor_2_appointed = False
        self.assessor_1_responded = False
        self.assessor_2_responded = False
        self.assessor_3_responded = False
        self.assessor_1_response = False
        self.assessor_1_invite_sent = False
        self.assessor_2_response = False
        self.assessor_2_invite_sent = False
        self.assessor_3_response = False
        self.assessor_3_invite_sent = False
        self.assessor_1_approved = False
        self.assessor_2_approved = False
        self.assessor_3_approved = False
        self.assessor_1_name=''
        self.assessor_1_email=''
        self.assessor_1_surname=''
        self.primary_supervisor = None
        self.assessor_2_name=''
        self.assessor_2_email=''
        self.assessor_2_surname=''
        self.comments = ''
        self.hdc_comments = ''
        self.assessor_1 = None
        self.assessor_2 = None
        self.assessor_3 = None

        self.delete_nomination_form()
        self.delete_jbs5_form()
        self.delete_jbs10_form()
        self.delete_sp_form()
        self.delete_notice_form()
        self.save()

    def delete_nomination_form(self):
        try: 
          form = getattr(self, "nomination_form")
          form.delete()
        except (AttributeError):
            return
    def delete_jbs5_form(self):
        try: 
          form = getattr(self, "jbs5_form")
          form.delete()
        except (AttributeError):
            return
    def delete_jbs10_form(self):
        try: 
          form = getattr(self, "jbs10_form")
          form.delete()
        except (AttributeError):
            return
    def delete_sp_form(self):
        try: 
          form = getattr(self, "sp_form")
          form.delete()
        except (AttributeError):
            return
    def delete_notice_form(self):
        try: 
          form = getattr(self, "notice_form")
          form.delete()
        except (AttributeError):
            return
        
    def get_assessor_2(self):
        try:
            return ExamminerProfile.objects.get(id=self.assessor_2)
        except:
            return None
    
    def get_assessor_3(self):
        try:
            return ExamminerProfile.objects.get(id=self.assessor_3)
        except:
            return None
    def can_submit_hdc(self):
        try:
            assert getattr(self, "sp_form"), "sp_form is not set"
            assert getattr(self, "jbs5_form"), "jbs5_form is not set"
            assert getattr(self, "jbs10_form"), "jbs10_form is not set"
            assert getattr(self, "notice_form"), "notice_form is not set"
            assert getattr(self, "nomination_form"), "nomination_form is not set"

        except (AssertionError, AttributeError) as e:
            print(e)
            return False

        print("all forms are set")

        sp_form = self.sp_form
        jbs5_form = self.jbs5_form
        jbs10_form = self.jbs10_form
        notice_form = self.notice_form
        nomination_form = self.nomination_form     
        if not (sp_form.supervisor_signed and sp_form.student_signed and 
                jbs5_form.supervisor_signed and jbs5_form.student_signed and
                jbs10_form.supervisor_signed and jbs10_form.student_signed and
                notice_form.supervisor_signed and notice_form.student_signed and
                nomination_form.supervisor_signed) and not self.title_approved:
            return False
        return True
    def sp_form_signed(self):
        try:
            assert getattr(self, "sp_form"), "sp_form is not set"
        except (AssertionError, AttributeError) as e:
            print(e)
            return False
        sp_form = self.sp_form
        if not (sp_form.supervisor_signed and sp_form.student_signed):
            return False
        return True
    def can_submit_jbs5(self):
       
        try:
            assert getattr(self, "jbs5_form"), "jbs5_form is not set"
        except (AssertionError, AttributeError) as e:
            print(e)
            return False
        jbs5_form = self.jbs5_form
        if not (jbs5_form.supervisor_signed and jbs5_form.student_signed) and not self.title_approved:
            return False
        return True
    # should go with jbs10
    def can_submit_notice(self):
        if not self.title_approved:
            return False
        try:
            assert getattr(self, "notice_form"), "notice_form is not set"
            assert getattr(self, "jbs10_form"), "jbs10_form is not set"
        except (AssertionError, AttributeError) as e:
            print(e)
            return False
        notice_form = self.notice_form
        jbs10_form = self.jbs10_form
        if not (jbs10_form.supervisor_signed and jbs10_form.student_signed):
            return False
        if not (notice_form.supervisor_signed and notice_form.student_signed):
            return False
        return True
    def cansubmit_nomination(self):
        if not self.title_approved:
            return False
        try:
            assert getattr(self, "nomination_form"), "nomination_form is not set"
        except (AssertionError, AttributeError) as e:
    
            return False
        nomination_form = self.nomination_form
        if not nomination_form.supervisor_signed:
            return False
        return True
    def should_show_jbs5_btn(self):
        return not self.title_approved and (self.project_status in [self.ProjectStatus.JBS5_Admin_declined,self.ProjectStatus.JBS5_HDC_declined, self.ProjectStatus.CREATED])
    def should_show_nomination_btn(self):
        return self.title_approved and (not self.nomination_form_submitted)
    
    def should_show_itent_btn(self):
        return self.title_approved and (not self.intent_form_submitted)
    
    def format_project_status(self):
        return self.ProjectStatus(self.project_status).label
    
    def reset_appointed_assessors(self):
        self.assessor_1_name = ''
        self.assessor_2_name = ''
        self.assessor_1_email = ''
        self.assessor_2_email = ''
        self.assessor_1_surname = ''
        self.assessor_2_surname = ''
        self.save()

    def __str__(self):
        return self.project_title