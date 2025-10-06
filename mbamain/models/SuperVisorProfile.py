from django.db import models

class supervisorProfile(models.Model):
    user = models.OneToOneField('mbamain.AUser', related_name='supervisor_profile', on_delete=models.CASCADE, null=False, blank=False)
    name = models.TextField(null=True, blank=True)
    surname = models.TextField(null=True, blank=True)  
    title = models.TextField(null=True, blank=True)  # e.g. Professor, Dr., etc.
    skills = models.TextField(null=True, blank=True)  # Store skills as a comma-separated string
    address = models.TextField(null=True, blank=True)  # Store skills as a comma-separated string
    department = models.TextField(null=True, blank=True)  # Store skills as a comma-separated string
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.TextField(null=True, blank=True)  # e.g. Lecturer, Senior Lecturer, etc.
    contact = models.TextField(null=True, blank=True)
    students = models.IntegerField(null=True, default=0) # hidden field
    def get_skills(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    def get_initials(self):
        c1 = self.name[0] if self.name else ''
        c2 = self.surname[0] if self.surname else ''
        return f'{c2}{c1}'.upper()
    def __str__(self):
        return f"{self.user.username}'s Profile"