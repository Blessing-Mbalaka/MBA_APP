import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import AUser, StudentProfile, ExamminerProfile, SupervisorProfile

# Clean all test data
test_prefixes = ['e_', 's_', 'sv_']
for prefix in test_prefixes:
    count = AUser.objects.filter(email__startswith=prefix).count()
    if count:
        AUser.objects.filter(email__startswith=prefix).delete()
        print(f"Deleted {count} users with prefix {prefix}")

# Clean orphaned profiles
orphaned = StudentProfile.objects.exclude(user__isnull=False).count()
if orphaned:
    StudentProfile.objects.exclude(user__isnull=False).delete()
    print(f"Deleted {orphaned} orphaned student profiles")

print("Cleanup complete - ready for testing")
