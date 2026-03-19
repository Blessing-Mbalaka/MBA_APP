#!/usr/bin/env python
"""
Enhanced test script to verify smart discipline-supervisor skills matching
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import AUser, Project, StudentProfile
from mbaAdmin.utils import supervisor_matches_discipline, get_discipline_keywords

print("=" * 70)
print("SMART MATCHING SYSTEM DIAGNOSTICS")
print("=" * 70)

# Check database state
print("\n1. Database State Check:")
student_count = AUser.objects.filter(user_type=AUser.UserType.STUDENT).count()
scholar_count = AUser.objects.filter(user_type=AUser.UserType.SCHOLAR).count()
project_count = Project.objects.count()

print(f"   Total Students: {student_count}")
print(f"   Total Supervisors (Scholars): {scholar_count}")
print(f"   Total Projects: {project_count}")

# Check test data
print("\n2. Searching for test data:")

# Try variations of username
possible_usernames = ['bmbalaka', 'Blessing', 'blessing', 'Mr Blessing', 'mbalaka']
blessing = None

for username in possible_usernames:
    blessing = AUser.objects.filter(username__icontains=username.lower()).first()
    if blessing:
        print(f"   ✓ Found user with username containing '{username}': {blessing.username}")
        break

if not blessing:
    # Try by email
    blessing = AUser.objects.filter(email__iexact='bmbalaka@uj.ac.za').first()
    if blessing:
        print(f"   ✓ Found user by email bmbalaka@uj.ac.za: {blessing.username}")

if not blessing and student_count > 0:
    blessing = AUser.objects.filter(user_type=AUser.UserType.STUDENT).first()
    print(f"   ℹ Using first student in database: {blessing.username} ({blessing.email})")

if blessing:
    try:
        student_profile = StudentProfile.objects.get(user=blessing)
        project = blessing.projects.first()
        
        if project:
            print(f"\n3. Student Details:")
            print(f"   Name: {blessing.first_name} {blessing.last_name}")
            print(f"   Email: {blessing.email}")
            print(f"   Username: {blessing.username}")
            print(f"   Project: {project.project_title}")
            print(f"   Discipline: '{project.discipline}'")
            
            # Test the matching logic
            print(f"\n4. Testing Smart Matching Logic:")
            keywords = get_discipline_keywords(project.discipline)
            print(f"   Keywords for '{project.discipline}': {keywords}")
            
            # Get all supervisors
            all_supervisors = AUser.objects.filter(user_type=AUser.UserType.SCHOLAR)
            print(f"\n   Total supervisors to check: {all_supervisors.count()}")
            
            if all_supervisors.count() > 0:
                print(f"\n   Supervisor Skills Sample (first 5):")
                for sup in all_supervisors[:5]:
                    skills = sup.supervisor_profile.skills or 'NO SKILLS'
                    print(f"   - {sup.first_name} {sup.last_name}: {skills}")
                
                # Find matches
                matching_supervisors = [
                    sup for sup in all_supervisors 
                    if supervisor_matches_discipline(sup.supervisor_profile.skills or '', project.discipline)
                ]
                
                print(f"\n5. MATCHING RESULTS:")
                print(f"   Found {len(matching_supervisors)} supervisors matching '{project.discipline}'")
                
                if matching_supervisors:
                    print(f"\n   Matched Supervisors (showing first 10):")
                    for i, sup in enumerate(matching_supervisors[:10], 1):
                        match = supervisor_matches_discipline(sup.supervisor_profile.skills or '', project.discipline)
                        print(f"   {i}. {sup.first_name} {sup.last_name}")
                        print(f"      Skills: {sup.supervisor_profile.skills}")
                        print(f"      Match: ✓")
                else:
                    print(f"\n   ✗ NO SUPERVISORS FOUND")
                    print(f"\n   DEBUGGING INFO:")
                    print(f"   - Discipline: '{project.discipline}'")
                    print(f"   - Keywords: {keywords}")
                    print(f"   - Testing with sample supervisors:")
                    
                    for sup in all_supervisors[:3]:
                        result = supervisor_matches_discipline(sup.supervisor_profile.skills or '', project.discipline)
                        print(f"     • {sup.first_name}: {sup.supervisor_profile.skills} -> {result}")
            else:
                print("   ✗ No supervisors in database")
        else:
            print(f"   ✗ Student {blessing.username} has no projects")
            
    except StudentProfile.DoesNotExist:
        print(f"   ✗ No StudentProfile found for {blessing.username}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("   ✗ Could not find Blessing Mbalaka or any student in database")

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
