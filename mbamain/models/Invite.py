from django.db import models

class Invite(models.Model):
    user = models.ForeignKey('mbamain.AUser', related_name='user_invites', on_delete=models.CASCADE, null=False, blank=False)
    invite_type = models.BooleanField(default=False) # True for assessors and False for supervisors
    project =  models.ForeignKey('mbamain.Project', null=True, related_name="projects_invites", blank=False, on_delete=models.DO_NOTHING)
    read = models.BooleanField(null=True, default=False)
    response = models.BooleanField(null=True)
    responeded_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.username}'s Profile"