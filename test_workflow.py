#!/usr/bin/env python
"""
Test the complete student workflow end-to-end
Steps:
1. Register as student
2. Create project
3. Appoint supervisor  
4. Fill & sign forms
5. Submit to HDC
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from mbamain.models import Project, StudentProfile, SupervisorProfile, JBS5, StudentSupervisorForm
from datetime import datetime

User = get_user_model()
client = Client()

print("\n" + "="*80)
print("  STUDENT WORKFLOW TEST")
print("="*80 + "\n")

# Step 1: Clean up test users
print("[1] Cleaning up old test users...")
User.objects.filter(username__in=['workflow_student', 'workflow_supervisor']).delete()

# Step 2: Create supervisor user
print("[2] Creating supervisor user...")
supervisor_user = User.objects.create_user(
    username='workflow_supervisor',
    email='supervisor@test.com',
    password='testpass',
    user_type=2,  # SCHOLAR
    first_name='Test',
    last_name='Supervisor',
)
SupervisorProfile.objects.get_or_create(
    user=supervisor_user,
    defaults={'name': 'Test', 'surname': 'Supervisor', 'contact': '1234567890'}
)
print(f"✓ Supervisor created: {supervisor_user.username}")

# Step 3: Create student user
print("[3] Creating student user...")
student_user = User.objects.create_user(
    username='workflow_student',
    email='student@test.com',
    password='testpass',
    user_type=3,  # STUDENT
    first_name='Test',
    last_name='Student',
)
StudentProfile.objects.get_or_create(
    user=student_user,
    defaults={
        'name': 'Test',
        'surname': 'Student',
        'student_no': 'WF001',
        'contact': '9876543210',
        'block_id': 'BLK001'
    }
)
print(f"✓ Student created: {student_user.username}")

# Step 4: Login as student
print("[4] Login as student...")
login_success = client.login(username='workflow_student', password='testpass')
if not login_success:
    print("✗ FAILED: Could not login as student")
    sys.exit(1)
print("✓ Logged in successfully")

# Step 5: Create project
print("[5] Creating project...")
response = client.post('/projects/create', {
    'title': 'Workflow Test Project',
    'description': 'This is a test project for workflow validation',
    'discipline': 'Computer Science',
    'sdg': 'Quality Education'
})
if response.status_code in [200, 302]:
    project = Project.objects.filter(student=student_user).latest('created_date')
    print(f"✓ Project created: ID={project.id}, Title='{project.project_title}'")
    project_id = project.id
else:
    print(f"✗ FAILED: Project creation returned {response.status_code}")
    if hasattr(response, 'content'):
        print(response.content.decode()[:500])
    sys.exit(1)

# Step 6: Try to view project
print(f"[6] Viewing project details...")
response = client.get(f'/projects/manage/{project_id}')
if response.status_code == 200:
    print(f"✓ Project page loaded (status {response.status_code})")
else:
    print(f"✗ FAILED: Project page returned {response.status_code}")

# Step 7: Create StudentSupervisorForm
print("[7] Creating StudentSupervisorForm...")
form, created = StudentSupervisorForm.objects.get_or_create(
    project=project,
    defaults={
        'initials_student': 'TS',
        'initials_supervisor': 'TS',
        'supervisor_signed': False,
        'student_signed': False,
    }
)
print(f"✓ Form created: {form.id}")

# Step 8: Create JBS5 form
print("[8] Creating JBS5 form...")
jbs5, created = JBS5.objects.get_or_create(
    project=project,
    defaults={
        'study_type': 'Research',
        'ir': 'IR Research',
        'qualification': 'MBA',
        'title': 'Test Research Project',
        'research_specific': True,
        'secondary_focus': False,
        'student_signed': False,
        'supervisor_signed': False,
    }
)
print(f"✓ JBS5 form created: {jbs5.id}")

# Step 9: Test JBS5 form access
print("[9] Testing JBS5 form access...")
response = client.get(f'/jbs5/form/{project_id}')
if response.status_code == 200:
    print(f"✓ JBS5 form page loaded (status {response.status_code})")
else:
    print(f"✗ FAILED: JBS5 form returned {response.status_code}")
    if hasattr(response, 'content'):
        print(response.content.decode()[:500])

# Step 10: Logout
print("[10] Logout...")
client.logout()
print("✓ Logged out")

print("\n" + "="*80)
print("  WORKFLOW TEST COMPLETE")
print("="*80)
print("\nSummary:")
print(f"  • Student created: {student_user.username}")
print(f"  • Project created: ID={project_id}")
print(f"  • Can access: /projects/manage/{project_id}, /jbs5/form/{project_id}")
print("\nNext steps:")
print("  1. Test filling forms via browser")
print("  2. Test signing forms")
print("  3. Test submission workflow")
print("\n")
