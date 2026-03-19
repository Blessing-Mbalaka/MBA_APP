import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import Project, ExamminerProfile
from mbaAdmin.utils import supervisor_matches_discipline

print("=" * 80)
print("ASSESSOR MATCHING FIX VERIFICATION")
print("=" * 80)

# Find project 17
try:
    project = Project.objects.get(id=17)
    print(f"\nProject Found: {project.project_title}")
    print(f"Discipline: {project.discipline}")
    
    # Get all examiners
    all_examiners = ExamminerProfile.objects.all()
    print(f"\nTotal Examiners in DB: {all_examiners.count()}")
    
    # Show all examiners and their skills
    print(f"\nAll Examiners & Skills:")
    for exam in all_examiners:
        print(f"  - {exam.name} {exam.surname}: {exam.skills}")
    
    # Apply smart matching
    matching_examiners = [
        exam for exam in all_examiners
        if supervisor_matches_discipline(exam.skills or '', project.discipline)
    ]
    
    print(f"\n[MATCHING RESULTS]")
    print(f"Assessors matching '{project.discipline}': {len(matching_examiners)}")
    
    if matching_examiners:
        print(f"\nMatched Assessors:")
        for i, exam in enumerate(matching_examiners, 1):
            print(f"{i}. {exam.name} {exam.surname}")
            print(f"   Skills: {exam.skills}")
            print(f"   Match: YES")
        
        print(f"\n[SUCCESS] Assessor matching is now working!")
    else:
        print(f"\n[FAILED] Still no matches found")
        
except Project.DoesNotExist:
    print("[ERROR] Project 17 not found in database")
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
