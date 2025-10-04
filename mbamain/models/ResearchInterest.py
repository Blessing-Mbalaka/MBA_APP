from django.db import models

class ResearchInterest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    