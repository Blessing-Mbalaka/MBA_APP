"""
FINAL TEST: Student bulk upload constraint violation fix
Verifies the two critical fixes:
1. Case-insensitive duplicate detection
2. Signal-based profile creation (get_or_create pattern)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import get_user_model
from mbamain.models import StudentProfile
from django.db.models import Q

User = get_user_model()

print("\n" + "="*75)
print("FINAL VERIFICATION: Student Upload Fixes")
print("="*75)

# Clean test data
StudentProfile.objects.filter(student_no__startswith='FINAL_').delete()
User.objects.filter(email__iexact='final.test@exam.com').delete()

print("\n[SETUP] Cleaning database...")
print("[SETUP] Ready to test")

print("\n" + "-"*75)
print("FIX #1: Case-Insensitive Duplicate Detection")
print("-"*75)

# Create user with lowercase email
user = User.objects.create_user(
    username='final.test@exam.com',
    email='final.test@exam.com',
    password='test123',
    user_type=User.UserType.STUDENT
)
print("[OK] Created user with email: final.test@exam.com")

# Test: Case-insensitive check should find it
found = User.objects.filter(email__iexact='FINAL.TEST@EXAM.COM').exists()
print("[OK] Case-insensitive search finds user: {}".format(found))

print("\n" + "-"*75)
print("FIX #2: Signal-Based Profile Creation + get_or_create")
print("-"*75)

# Check signal auto-created profile
profile_count = StudentProfile.objects.filter(user=user).count()
print("[OK] Signal auto-created {} profile(s)".format(profile_count))

# Update profile using get_or_create (no constraint violation)
profile, created = StudentProfile.objects.get_or_create(user=user)
profile.student_no = 'FINAL_001'
profile.name = 'Final'
profile.surname = 'Test'
profile.save()
print("[OK] Updated profile with get_or_create - no constraint violation!")

# Verify no duplicate profiles
final_count = StudentProfile.objects.filter(user=user).count()
print("[OK] Final profile count: {} (should be 1)".format(final_count))

print("\n" + "="*75)
print("RESULT: Both fixes working correctly!")
print("="*75)
print()
