from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class AUser(AbstractUser):
    class UserType(models.IntegerChoices):
        MAIN_ADMIN = 0, # this admin can manage all users including the admins
        ADMIN = 1, 
        SCHOLAR = 2, 
        STUDENT = 3, 
        EXAMINER = 4, 
        HDC = 5, 
    class RoleType(models.IntegerChoices):
        EXAMINER = 0
        SUPERVISOR = 1
        BOTH = 2
    user_type = models.IntegerField(choices=UserType.choices, default=UserType.STUDENT)
    role_type = models.IntegerField(choices=RoleType.choices, null=True, blank=True)
    has_profile = models.BooleanField(default=False)
    has_signature = models.BooleanField(default=False)
    has_cv = models.BooleanField(default=False)
    
    def set_user_type(self, user_type):
        if user_type in [self.UserType.MAIN_ADMIN, self.UserType.ADMIN, self.UserType.SCHOLAR, self.UserType.STUDENT, self.UserType.EXAMINER]:
            self.user_type = user_type
        else:
            raise ValueError("Invalid user type")
    def set_role_type(self, role_type):
        if role_type in [self.RoleType.EXAMINER, self.RoleType.SUPERVISOR, self.RoleType.BOTH]:
            self.role_type = role_type
        else:
            raise ValueError("Invalid role type")
    def get_weeks(self):
        last = self.last_login if self.last_login else timezone.now()
        diff = timezone.now() - last
        return diff.days // 7 
        # return diff.total_seconds() // 60 # for testing only, returns minutes since last login
    def set_has_profile(self, has_profile):
        self.has_profile = has_profile
    def set_has_signature(self, has_signature):
        self.has_signature = has_signature
    def is_admin(self):
        return self.user_type == self.UserType.ADMIN or self.user_type == self.UserType.MAIN_ADMIN
    def is_scholar(self):
        return self.user_type == self.UserType.SCHOLAR
    def is_student(self):
        return self.user_type == self.UserType.STUDENT
    def is_examiner(self):
        return self.role_type == self.RoleType.EXAMINER
    def is_hdc(self):
        return self.user_type == self.UserType.HDC
    def is_supervisor(self):
        return self.role_type == self.RoleType.SUPERVISOR or self.role_type == self.RoleType.BOTH
    def is_main_admin(self):
        return self.user_type == self.UserType.MAIN_ADMIN
    def set_active(self, is_active):
        self.is_active = is_active
    def set_temp_password(self, temp_password):
        self.set_password(temp_password)
    def __str__(self):
        return f"{self.email} "
    