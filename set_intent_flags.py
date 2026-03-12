#!/usr/bin/env python
"""
Set intent form submitted flag on test data
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

print("\n=== Setting Intent Form Data ===\n", file=sys.stderr)

# Get all test students
test_students = list(User.objects.filter(username__startswith='inject_test_student').order_by('id')[:5])

if len(test_students) == 0:
    print("ERROR: No test students found! Run inject_test_data.py first", file=sys.stderr)
    sys.exit(1)
else:
    count = 0
    for i, student in enumerate(test_students, 1):
        try:
            proj = Project.objects.filter(student=student).first()
            if proj:
                proj.intent_form_submitted = True
                proj.intent_form_approved = False
                proj.save()
                count += 1
                print(f"[OK] Student {i}: {student.email}", file=sys.stderr)
                print(f"     Project: {proj.project_title}", file=sys.stderr)
                print(f"     Intent Form Submitted: True\n", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] {str(e)}\n", file=sys.stderr)
    
    print(f"\n=== COMPLETE ===", file=sys.stderr)
    print(f"Updated {count} projects with intent form submitted", file=sys.stderr)
    print(f"Visit: http://127.0.0.1:8000/admin/intent/submitted/\n", file=sys.stderr)
