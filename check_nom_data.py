#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import Project, NominationForm, AUser, StudentProfile
from django.db.models import Q

# Find test students
test_students = AUser.objects.filter(username__startswith='inject_test_student_')
print(f"Test students found: {test_students.count()}")
for s in test_students:
    print(f"  - {s.username} (ID: {s.id})")
    # Check if they have student profile
    try:
        profile = StudentProfile.objects.get(user=s)
        print(f"    Student Profile: {profile.student_no} - Block {profile.block_id}")
    except:
        print(f"    ❌ NO StudentProfile")

# Check all projects with nomination submitted
print("\n" + "="*60)
print("Projects with nomination_form_submitted=True:")
projects = Project.objects.filter(
    Q(nomination_form_submitted=True) | Q(nomination_form_hdc_verified=True)
)
print(f"Total: {projects.count()}")
for p in projects:
    print(f"  - Project {p.id}: {p.project_title}")
    print(f"    Student: {p.student.username if p.student else 'DELETED'}")
    print(f"    nomination_form_submitted={p.nomination_form_submitted}, hdc_verified={p.nomination_form_hdc_verified}")

# Check all NominationForms
print("\n" + "="*60)
print("All NominationForm records:")
nom_forms = NominationForm.objects.all()
print(f"Total: {nom_forms.count()}")
for nf in nom_forms:
    print(f"  - Project {nf.project_id}: {nf.co_supervisor_full_names}")
