import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import AUser

count = 0
for user in AUser.objects.filter(email__contains='test.mba.local'):
    user.username = user.email
    user.save()
    count += 1

print(f"✓ Updated {count} test users")

# Verify
for user in AUser.objects.filter(email__contains='test.mba.local')[:3]:
    print(f"{user.email}: username={user.username}")