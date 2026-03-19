import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import AUser

AUser.objects.filter(email__startswith='e_').delete()
AUser.objects.filter(email__startswith='s_').delete()
AUser.objects.filter(email__startswith='sv_').delete()
AUser.objects.filter(username='testadmin').delete()

print("Database cleaned")
