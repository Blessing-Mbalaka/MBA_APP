import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import AUser

print("=" * 70)
print("POPULATING SUPERVISOR SKILLS FOR TESTING")
print("=" * 70)

supervisors = AUser.objects.filter(user_type=AUser.UserType.SCHOLAR)
skills_list = [
    'Machine Learning, Data Science',
    'Cloud Computing, DevOps',
    'Cybersecurity, Network Architecture',
    'Business Analytics, Finance',
    'Digital Marketing, Brand Strategy'
]

print(f"\nFound {supervisors.count()} supervisors")
print(f"Assigning skills from pattern: {skills_list}\n")

for i, supervisor in enumerate(supervisors):
    skills = skills_list[i % len(skills_list)]
    prof = supervisor.supervisor_profile
    prof.skills = skills
    prof.save()
    print(f"✓ {supervisor.username}: {skills}")

print(f"\n✓ Updated {supervisors.count()} supervisors with skills")
print("=" * 70)
