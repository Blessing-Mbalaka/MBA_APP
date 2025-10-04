from django.db import models

class Signature(models.Model):
    img_path = models.ImageField(upload_to='signatures/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField('mbamain.AUser', on_delete=models.CASCADE, null=False, blank=False)