from django.db import models


class Cv(models.Model):
    user = models.OneToOneField('mbamain.AUser', on_delete=models.CASCADE, null=False, blank=False, related_name="cv")
    cv_file = models.FileField(upload_to='cvs/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s CV"