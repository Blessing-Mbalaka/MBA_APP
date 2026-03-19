import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import AUser, Project

# Show supervisors and their skills
supervisors = AUser.objects.filter(user_type=AUser.UserType.SCHOLAR)
print(f"Total supervisors in DB: {supervisors.count()}")
for sup in supervisors[:5]:
    skills = sup.supervisor_profile.skills if sup.supervisor_profile else "NO PROFILE"
    print(f"  - {sup.username}: {skills}")

# Show students with projects
students = AUser.objects.filter(user_type=AUser.UserType.STUDENT)
print(f"\nTotal students in DB: {students.count()}")

projects = Project.objects.all()
print(f"Total projects in DB: {projects.count()}")

if projects.exists():
    print("\nFirst 3 projects:")
    for proj in projects[:3]:
        print(f"  Project: {proj.project_title}")
        print(f"    Discipline: {proj.discipline}")
        print(f"    Primary Supervisor ID: {proj.primary_supervisor}")
        if proj.primary_supervisor:
            try:
                sup = AUser.objects.get(user_id=proj.primary_supervisor)
                print(f"    Assigned to: {sup.first_name} {sup.last_name}")
            except:
                print(f"    ERROR: Supervisor ID {proj.primary_supervisor} not found")
