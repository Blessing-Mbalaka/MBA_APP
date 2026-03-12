#!/usr/bin/env python
"""
Fix Intent Form Data - Inject test projects with intent form submitted
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import get_user_model
from mbamain.models import Project, StudentProfile

User = get_user_model()

print("\n" + "="*80)
print("INTENT FORM DATA FIX - COMPREHENSIVE INJECTION")
print("="*80 + "\n")

# Step 1: Check if we have test students
print("Step 1: Checking for test students...")
test_students = User.objects.filter(username__startswith='inject_test_student').order_by('id')
print(f"Found {test_students.count()} test students\n")

if test_students.count() == 0:
    print("ERROR: No test students found!")
    print("Please run: python inject_test_data.py\n")
    exit(1)

# Step 2: Update projects with intent form submitted
print("Step 2: Updating projects with intent_form_submitted=True...")
count = 0
for i, student in enumerate(test_students[:5], 1):
    try:
        project = Project.objects.filter(student=student).first()
        if project:
            # Set the intent form submitted flag
            project.intent_form_submitted = True
            project.intent_form_approved = False
            project.save()
            count += 1
            
            # Get student profile for display
            profile = StudentProfile.objects.get(user=student)
            print(f"  [{i}] {profile.name} {profile.surname} - {student.username}")
            print(f"      Project: {project.project_title}")
            print(f"      Status: intent_form_submitted = True\n")
    except Exception as e:
        print(f"  ERROR: {str(e)}\n")

print(f"Updated {count} projects\n")

# Step 3: Verify the data
print("Step 3: Verifying data in database...")
total_intent_projects = Project.objects.filter(intent_form_submitted=True).count()
print(f"Total projects with intent_form_submitted=True: {total_intent_projects}\n")

if total_intent_projects > 0:
    print("Sample data:")
    for proj in Project.objects.filter(intent_form_submitted=True)[:3]:
        print(f"  - {proj.student.username}: {proj.project_title}")
else:
    print("WARNING: No projects found with intent_form_submitted=True")

print("\n" + "="*80)
print("NEXT STEPS:")
print("="*80)
print("1. Restart the Django server (kill and restart if running)")
print("2. Visit: http://127.0.0.1:8000/admin/intent/submitted/")
print("3. You should now see the test data displayed\n")
