from django.db import models

class ExamminerProfile(models.Model):
    #Make this a foreignkey reference, and create a profile ID as PK so we don't repeat logic, this makes no sense!!!!
    #We can't be storing 
    user = models.OneToOneField('mbamain.AUser', related_name='examiner_profile', on_delete=models.CASCADE, null=False, blank=False)
    name = models.TextField(null=True, blank=True)
    surname = models.TextField(null=True, blank=True)  
    title = models.TextField( null=True, blank=True)  # e.g. Professor, Dr., etc.
    qualification = models.TextField(null=True, blank=True) 
    affiliation = models.TextField( null=True, blank=True)  # e.g. University, Institution
    street_address = models.TextField(null=True, blank=True)  # Street address for contact
    cell_phone = models.TextField(null=True, blank=True)  # Cell phone number
    skills = models.TextField(null=True, blank=True)  # Cell phone number
    email = models.EmailField(null=True, blank=True)  # Email address for contact
    number_of_students_supervised = models.PositiveIntegerField(default=0)  # Number of students examined
    current_affiliation = models.TextField(null=True)  # Current affiliation
    number_publications = models.PositiveIntegerField(default=0)  # Number of publications
    approved_before = models.BooleanField(default=False)  # Number of students assessed
    international_assessor = models.BooleanField(default=False)  # Whether the examiner is an international assessor
    academic_experience = models.PositiveBigIntegerField(default=0)  # Academic experience in years
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the profile was created
    
    def __str__(self):
        return f"{self.name}'s Profile"