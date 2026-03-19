import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import AUser, Project, SupervisorProfile

print('=== SUPERVISORS WITH SKILLS ===')
supervisors = AUser.objects.filter(user_type=AUser.UserType.SCHOLAR)
for sup in supervisors[:10]:
    prof = sup.supervisor_profile
    skills_status = 'HAS SKILLS' if prof.skills else 'NO SKILLS'
    print(f'{sup.first_name} {sup.last_name}: {skills_status}')
    if prof.skills:
        print(f'  Skills: {prof.skills}')

print(f'\nTotal supervisors: {supervisors.count()}')
with_skills = sum(1 for s in supervisors if s.supervisor_profile.skills)
print(f'Supervisors with assigned skills: {with_skills}')

print('\n=== STUDENTS WITH PROJECTS (showing first 5) ===')
students = AUser.objects.filter(user_type=AUser.UserType.STUDENT)
student_count = 0
for student in students[:5]:
    try:
        prof = student.student_profile
        projects = Project.objects.filter(student=prof)
        if projects.exists():
            student_count += 1
            print(f'\nStudent {student_count}: {student.first_name} {student.last_name} ({student.email})')
            for proj in projects:
                print(f'  Project Discipline: {proj.discipline}')
                if proj.primary_supervisor:
                    try:
                        sup = AUser.objects.get(user_id=proj.primary_supervisor)
                        sup_prof = sup.supervisor_profile
                        print(f'  Assigned Supervisor: {sup.first_name} {sup.last_name}')
                        print(f'  Supervisor Skills: {sup_prof.skills if sup_prof.skills else "NONE"}')
                    except:
                        print(f'  Assigned Supervisor ID {proj.primary_supervisor} not found')
                else:
                    print(f'  No supervisor assigned')
    except Exception as e:
        print(f'Error for {student.first_name}: {e}')

print(f'\nTotal students: {students.count()}')
print(f'Students with projects: {student_count}')
