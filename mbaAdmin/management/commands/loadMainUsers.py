from django.core.management.base import BaseCommand
from mbamain.models import AUser


class Command(BaseCommand):
    help = "create an admin or hdc user if not exists"

    def handle(self, *args, **kwargs):
        try:
            user = AUser.objects.create_user(username="admin@uj.ac.za", email="admin@uj.ac.za", password="password")
             
            user.user_type = AUser.UserType.MAIN_ADMIN
            user.save()
        except Exception as e:
            print("Admin user already exists")    
        try:
            user = AUser.objects.create_user(username="hdc@uj.ac.za", email="hdc@uj.ac.za", password="password")
            user.user_type = AUser.UserType.HDC
            user.save()
        except Exception as e:
            print("HDC user already exists")
        print("Default users created/verified successfully")
         
