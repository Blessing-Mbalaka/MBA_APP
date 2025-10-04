from django.db import models
from django.utils import timezone

class PasswordResetToken(models.Model):
    token = models.CharField(max_length=8, unique=False, null=False, blank=False)
    created_date = models.DateTimeField(null=False)
    max_time = models.IntegerField(null=False)
    user = models.OneToOneField('mbamain.AUser', on_delete=models.CASCADE, null=False, blank=False)
    def has_expired(self):
        diff = timezone.now() - self.created_date
        return diff.total_seconds() // 60 > self.max_time
    def generate_token():
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
   