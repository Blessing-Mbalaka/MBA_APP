#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

print("\n=== DIAGNOSTIC CHECK ===\n")

# Check test students exist
students = User.objects.filter(username__startswith='inject_test_student').order_by('id')
print(f"Test students: {students.count()}")
for s in students[:3]:
    print(f"  - {s.username} (ID: {s.id})")

# Check if they have projects
print(f"\nProjects for test students:")
for s in students[:3]:
    projs = Project.objects.filter(student=s)
    print(f"  - {s.username}: {projs.count()} projects")
    for p in projs:
        print(f"    • {p.project_title} (intent_submitted={p.intent_form_submitted})")

# Check total projects in DB
all_projs = Project.objects.all()
print(f"\nTotal projects in database: {all_projs.count()}")

# Try to manually update
print(f"\n=== ATTEMPTING UPDATE ===\n")
for s in students[:5]:
    projs = Project.objects.filter(student=s)
    for p in projs:
        p.intent_form_submitted = True
        p.intent_form_approved = False
        p.save()
        print(f"Updated: {s.username} -> {p.project_title}")

# Verify
count = Project.objects.filter(intent_form_submitted=True).count()
print(f"\nFinal count of intent submitted projects: {count}")
