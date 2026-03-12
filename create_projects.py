#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

print("\n=== Creating Projects for Test Students ===\n")

disciplines = ['Machine Learning', 'Cloud Computing', 'Cybersecurity', 'Business Analytics', 'Digital Marketing']
statuses = [
    Project.ProjectStatus.CREATED,
    Project.ProjectStatus.HDC_SUBMITTED,
    Project.ProjectStatus.JBS5_submitted,
]

# Get test students
students = User.objects.filter(username__startswith='inject_test_student').order_by('id')

print(f"Creating projects for {students.count()} students...\n")

created = 0
for i, student in enumerate(students[:5], 1):
    try:
        # Check if project already exists
        existing = Project.objects.filter(student=student).first()
        if existing:
            print(f"  [{i}] {student.username} - Project already exists")
            continue
        
        # Create project
        project = Project.objects.create(
            student=student,
            project_title=f"Research on {disciplines[i % len(disciplines)]}",
            project_description=f"Study of {disciplines[i % len(disciplines)]} technologies",
            discipline=disciplines[i % len(disciplines)],
            project_status=statuses[i % len(statuses)],
            qualification='MBA',
            sdg_goal='Goal 8: Decent Work and Economic Growth',
            intent_form_submitted=True,  # Set intent form submitted
            intent_form_approved=False
        )
        
        created += 1
        print(f"  [{i}] ✓ {student.username} - Created project")
        print(f"      intent_form_submitted=True\n")
        
    except Exception as e:
        print(f"  [{i}] ✗ {student.username} - Error: {str(e)}\n")

print(f"Created: {created} projects\n")

# Verify
intent_count = Project.objects.filter(intent_form_submitted=True).count()
print(f"Total projects with intent submitted: {intent_count}\n")

print("SUCCESS! Now:")
print("1. Restart Django server")
print("2. Visit: http://127.0.0.1:8000/admin/intent/submitted/")
