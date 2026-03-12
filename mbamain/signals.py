from django.db.models.signals import post_save
from django.dispatch import receiver
from mbamain.models import AUser, StudentProfile, SupervisorProfile, ExamminerProfile

@receiver(post_save, sender=AUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == AUser.UserType.STUDENT:
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.user_type == AUser.UserType.SCHOLAR:
            SupervisorProfile.objects.get_or_create(user=instance)
        elif instance.user_type == AUser.UserType.EXAMINER:
            ExamminerProfile.objects.get_or_create(user=instance)