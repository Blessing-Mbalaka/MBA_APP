import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import AUser, Project
from mbaAdmin.utils import supervisor_matches_discipline, get_discipline_keywords

print("=" * 80)
print("SMART MATCHING TEST - With Supervisor Skills Populated")
print("=" * 80)

# Verify supervisors have skills now
supervisors = AUser.objects.filter(user_type=AUser.UserType.SCHOLAR)
print(f"\n1. Supervisor Skills Status:")
print(f"   Total supervisors: {supervisors.count()}")

has_skills = 0
for sup in supervisors:
    if sup.supervisor_profile.skills:
        has_skills += 1

print(f"   Supervisors with skills: {has_skills}/{supervisors.count()}")

# Find Blessing Mbalaka
print(f"\n2. Finding Blessing Mbalaka...")
blessing = AUser.objects.filter(email__iexact='bmbalaka@uj.ac.za').first()

if blessing:
    project = blessing.projects.first()
    if project:
        print(f"   [OK] Name: {blessing.first_name} {blessing.last_name}")
        print(f"   [OK] Email: {blessing.email}")
        print(f"   [OK] Project: {project.project_title}")
        print(f"   [OK] Discipline: {project.discipline}")
        
        # Test smart matching
        print(f"\n3. Testing Smart Matching for '{project.discipline}':")
        keywords = get_discipline_keywords(project.discipline)
        print(f"   Keywords: {keywords}")
        
        # Get all supervisors and filter using smart matching
        all_supervisors = AUser.objects.filter(
            user_type=AUser.UserType.SCHOLAR
        ).order_by('supervisor_profile__students')
        
        matching = [
            sup for sup in all_supervisors
            if supervisor_matches_discipline(sup.supervisor_profile.skills or '', project.discipline)
        ]
        
        print(f"\n4. RESULTS:")
        print(f"   Found {len(matching)} supervisors matching '{project.discipline}'")
        
        if matching:
            print(f"\n   Matching supervisors:")
            for i, sup in enumerate(matching[:5], 1):
                print(f"   {i}. {sup.username}")
                print(f"      Skills: {sup.supervisor_profile.skills}")
                result = supervisor_matches_discipline(sup.supervisor_profile.skills or '', project.discipline)
                print(f"      Match: [YES] {result}")
            
            print(f"\n[SUCCESS] Smart matching is working!")
        else:
            print(f"   [FAILED] No supervisors found")
            print(f"\n   DEBUG INFO:")
            print(f"   Discipline: '{project.discipline}'")
            print(f"   Keywords: {keywords}")
            print(f"   Sample supervisors:")
            for sup in all_supervisors[:3]:
                match = supervisor_matches_discipline(sup.supervisor_profile.skills or '', project.discipline)
                print(f"     - {sup.username}: {sup.supervisor_profile.skills} -> {match}")
    else:
        print(f"   [Error] No project for Blessing")
else:
    print(f"   [Error] Blessing Mbalaka not found")
    
print("\n" + "=" * 80)
