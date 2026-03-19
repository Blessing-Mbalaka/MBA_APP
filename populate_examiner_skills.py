import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import ExamminerProfile

print("=" * 70)
print("POPULATING EXAMINER SKILLS FOR ASSESSMENT MATCHING")
print("=" * 70)

examiners = ExamminerProfile.objects.all()
skills_list = [
    'Machine Learning, Data Science',
    'Cloud Computing, DevOps',
    'Cybersecurity, Network Architecture',
    'Business Analytics, Finance',
    'Digital Marketing, Brand Strategy'
]

print(f"\nFound {examiners.count()} examiners")
print(f"Assigning skills from pattern: {skills_list}\n")

for i, examiner in enumerate(examiners):
    skills = skills_list[i % len(skills_list)]
    examiner.skills = skills
    examiner.save()
    name = f"{examiner.name} {examiner.surname}" if examiner.name else examiner.email
    print(f"[OK] {name}: {skills}")

print(f"\n[SUCCESS] Updated {examiners.count()} examiners with skills")
print("=" * 70)
