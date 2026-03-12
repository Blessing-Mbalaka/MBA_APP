#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import Project, NominationForm, AUser
from django.utils import timezone

# Get existing test students
test_students = AUser.objects.filter(username__startswith='inject_test_student_')[:5]

if not test_students.exists():
    print("❌ No test students found! Run inject_test_data.py first.")
    exit(1)

# Get first supervisor for projects
supervisors = AUser.objects.filter(username__startswith='inject_test_supervisor_')
if not supervisors.exists():
    print("❌ No test supervisors found! Run inject_test_data.py first.")
    exit(1)

supervisor = supervisors.first()

print(f"✅ Found {test_students.count()} test students")
print(f"✅ Found {supervisors.count()} test supervisors")

# Create nomination test data
created_count = 0
updated_count = 0
for student in test_students:
    # Create or get project for this student
    project, created = Project.objects.get_or_create(
        student=student,
        defaults={
            'project_title': f'Research Nomination Test Project for {student.first_name}',
            'project_description': f'Test project for nomination form submission - {student.username}',
            'primary_supervisor': supervisor.id,
            'discipline': 'Machine Learning',
            'nomination_form_submitted': True,
            'created_date': timezone.now(),
        }
    )
    
    # Ensure nomination_form_submitted is True (in case project already existed)
    if not project.nomination_form_submitted:
        project.nomination_form_submitted = True
        project.save()
        updated_count += 1
        print(f"  → Updated existing project for {student.username} - set nomination_form_submitted=True")
    
    if created:
        print(f"  → Created new project for {student.username}")
        created_count += 1
    
    # Create NominationForm if it doesn't exist
    nomination_form, form_created = NominationForm.objects.get_or_create(
        project=project,
        defaults={
            'co_supervisor_full_names': f'Dr. Test Co-Supervisor for {student.first_name}',
            'co_supervisor_department': 'Engineering',
            'co_supervisor_phone': '+27123456789',
            'co_supervisor_email': f'cosupervisor_{student.username}@university.ac.za',
            'degree': 'MEng (Coursework)',
            'qualification': 'PhD, MSc',
            'supervisor_signed': True,
        }
    )
    
    if form_created:
        print(f"  → Created nomination form for {student.username}")
    else:
        print(f"  → Nomination form already exists for {student.username}")

print(f"\n✅ Nomination test data injection complete!")
print(f"   New projects created: {created_count}")
print(f"   Existing projects updated: {updated_count}")
print(f"   View at: http://127.0.0.1:8000/admin/nominations/")
