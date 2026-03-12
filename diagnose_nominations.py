#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import Project, NominationForm, AUser

# Check test students
test_students = AUser.objects.filter(username__startswith='inject_test_student_')
print(f"✅ Found {test_students.count()} test students")

# Check projects for test students
for student in test_students:
    projects = Project.objects.filter(student=student)
    print(f"\n📋 Student: {student.username}")
    print(f"   Total projects: {projects.count()}")
    
    for project in projects:
        print(f"   - Project ID: {project.id}")
        print(f"     Title: {project.project_title}")
        print(f"     nomination_form_submitted: {project.nomination_form_submitted}")
        print(f"     nomination_form_hdc_verified: {project.nomination_form_hdc_verified}")
        print(f"     Primary supervisor: {project.primary_supervisor}")
        
        # Check nomination form
        try:
            nom_form = NominationForm.objects.get(project=project)
            print(f"     ✅ NominationForm exists")
            print(f"        Co-supervisor: {nom_form.co_supervisor_full_names}")
        except NominationForm.DoesNotExist:
            print(f"     ❌ NO NominationForm found")

# Count all nominations
all_nominations = Project.objects.filter(
    nomination_form_submitted=True
).count()
print(f"\n\n📊 Total projects with nomination_form_submitted=True: {all_nominations}")

# Check if any nominations exist
all_nom_forms = NominationForm.objects.all()
print(f"📊 Total NominationForm records: {all_nom_forms.count()}")
