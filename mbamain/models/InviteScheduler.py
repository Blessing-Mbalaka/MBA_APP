from django.db import models
from django.utils import timezone

class InviteScheduler(models.Model):
    last_sent_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created = models.BooleanField(default=True, null=True)
    def should_send(self):
        diff = timezone.now() - self.last_sent_date
        return diff.total_seconds() // 60 >= 1 # for testing purposes only
        # return diff.days >= 3
    def __str__(self):
        pass