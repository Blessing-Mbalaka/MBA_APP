from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField('mbamain.AUser', related_name='student_profile', on_delete=models.CASCADE, null=False, blank=False)
    name = models.TextField(null=True, blank=True)
    surname = models.TextField(null=True, blank=True)  
    title = models.TextField(null=True, blank=True)  # e.g. Mr., Ms., etc.
    contact = models.TextField(null=True, blank=True)  
    student_no = models.TextField(null=True, blank=True)  # Student number, if applicable
    secondary_email = models.EmailField(null=True, blank=True)  # Secondary email address for contact  
    module =  models.TextField(null=True, blank=True) 
    block_id = models.TextField(null=False, blank=True)  # Block ID for the student
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the profile was created
    degree = models.TextField(null=True,default="MBA")
    address = models.TextField(null=True)
    def get_initials(self):
        c1 = self.name[0] if self.name else ''
        c2 = self.surname[0] if self.surname else ''
        return f'{c2}{c1}'.upper()
    def __str__(self):
        return f"{self.user.username}'s Profile"