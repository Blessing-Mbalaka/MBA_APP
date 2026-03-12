import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

# Get test students
students = list(User.objects.filter(username__startswith='inject_test_student').order_by('id')[:5])

print(f"Found {len(students)} test students")

# Update their projects
updated = 0
for student in students:
    proj = Project.objects.filter(student=student).first()
    if proj:
        proj.intent_form_submitted = True
        proj.intent_form_approved = False
        proj.save()
        updated += 1
        print(f"Updated: {student.email}")

print(f"\nTotal updated: {updated}")
print(f"Total projects with intent submitted: {Project.objects.filter(intent_form_submitted=True).count()}")
