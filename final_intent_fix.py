#!/usr/bin/env python
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.cache import cache
from mbamain.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

# Clear Django cache
cache.clear()
print("✓ Cleared Django cache")

# Get students
students = User.objects.filter(username__startswith='inject_test_student').order_by('id')[:5]
print(f"✓ Found {students.count()} test students")

# Update projects
for student in students:
    proj = Project.objects.filter(student=student).update(
        intent_form_submitted=True,
        intent_form_approved=False
    )

# Verify
count = Project.objects.filter(intent_form_submitted=True).count()
print(f"✓ Total projects with intent submitted: {count}")

if count > 0:
    print("\nData has been set! Now:")
    print("1. RESTART the Django server")
    print("2. Visit: http://127.0.0.1:8000/admin/intent/submitted/")
else:
    print("\nERROR: Could not set intent data")
