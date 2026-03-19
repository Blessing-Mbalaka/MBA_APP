#!/usr/bin/env python
"""Verify supervisor_view imports work correctly"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

print("=" * 80)
print("IMPORT VERIFICATION")
print("=" * 80)

# Test importing supervisor_view
print("\n[1] Testing supervisor_view import...")
try:
    from mbamain.views import supervisor_view
    print("    [SUCCESS] supervisor_view imported without errors")
except ImportError as e:
    print(f"    [FAILED] {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test that supervisor_matches_discipline is available
print("\n[2] Testing supervisor_matches_discipline availability...")
try:
    from mbaAdmin.utils.shortcuts import supervisor_matches_discipline
    print("    [SUCCESS] supervisor_matches_discipline is available")
    print(f"    Function signature: {supervisor_matches_discipline}")
except ImportError as e:
    print(f"    [FAILED] {str(e)}")
    exit(1)

# Test the logic
print("\n[3] Testing smart matching logic...")
from mbamain.models import Project, ExamminerProfile

project = Project.objects.get(id=23)
print(f"    Project: {project.project_title}")
print(f"    Discipline: {project.discipline}")

all_examiners = ExamminerProfile.objects.all()
matching = [
    exam for exam in all_examiners
    if supervisor_matches_discipline(exam.skills or '', project.discipline)
]

print(f"    Found {len(matching)} matching assessors")
for exam in matching:
    print(f"      - {exam.name} {exam.surname}: {exam.skills}")

if len(matching) > 0:
    print("\n[SUCCESS] Assessor matching is working!")
else:
    print("\n[WARNING] No matching assessors found")

print("=" * 80)
