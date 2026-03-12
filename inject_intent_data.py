#!/usr/bin/env python
"""
Quick Intent Form Test Data Injection
Creates a single student "Tobey Mbatoa" with a project that has submitted intent form
Usage: python inject_intent_data.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import get_user_model
from mbamain.models import StudentProfile, SupervisorProfile, Project

User = get_user_model()

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def main():
    print(f"\n{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BLUE}{'INTENT FORM TEST DATA INJECTION':^80}{Colors.END}")
    print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")
    
    # Delete old data if exists
    username = "tobey_mbatoa"
    print(f"{Colors.YELLOW}Checking for existing user...{Colors.END}")
    try:
        old_user = User.objects.get(username=username)
        Project.objects.filter(student=old_user).delete()
        old_user.delete()
        print(f"{Colors.GREEN}[OK] Old user cleaned{Colors.END}\n")
    except User.DoesNotExist:
        print(f"{Colors.GREEN}[OK] No old data found{Colors.END}\n")
    
    try:
        # Create student user
        print(f"{Colors.BLUE}Creating student: Tobey Mbatoa...{Colors.END}")
        user = User.objects.create_user(
            username=username,
            email='tobey.mbatoa@test.mba.local',
            password='testpass123',
            user_type=User.UserType.STUDENT,
            is_staff=False,
            has_profile=True
        )
        print(f"  {Colors.GREEN}[OK]{Colors.END} User created: {user.email}\n")
        
        # Create student profile
        print(f"{Colors.BLUE}Creating student profile...{Colors.END}")
        student_profile = StudentProfile.objects.create(
            user=user,
            name='Tobey',
            surname='Mbatoa',
            title='Mr.',
            student_no='STU99999',
            contact='+1-555-9999',
            module='MBA',
            block_id='BLOCK_TEST',
            degree='MBA',
            address='123 Intent Street, Test University'
        )
        print(f"  {Colors.GREEN}[OK]{Colors.END} Profile created\n")
        
        # Create project with intent form submitted
        print(f"{Colors.BLUE}Creating project with submitted intent form...{Colors.END}")
        project = Project.objects.create(
            student=user,
            project_title='Advanced Research in Business Intelligence and Analytics',
            project_description='A comprehensive study of business intelligence systems and their application in modern enterprises.',
            discipline='Business Analytics, Finance',
            project_status=Project.ProjectStatus.Notice_submitted,
            qualification='MBA',
            sdg_goal='Goal 8: Decent Work and Economic Growth',
            intent_form_submitted=True,  # This is the key flag!
            intent_form_approved=False
        )
        print(f"  {Colors.GREEN}[OK]{Colors.END} Project created\n")
        
        # Print summary
        print(f"{Colors.BLUE}{'='*80}{Colors.END}")
        print(f"{Colors.BLUE}{'INJECTION COMPLETE':^80}{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")
        
        print(f"{Colors.YELLOW}Test Data:{Colors.END}")
        print(f"  * Student Name: Tobey Mbatoa")
        print(f"  * Student Email: tobey.mbatoa@test.mba.local")
        print(f"  * Username: tobey_mbatoa")
        print(f"  * Password: testpass123")
        print(f"  * Student Number: STU99999")
        print(f"  * Block: BLOCK_TEST")
        print(f"  * Project: {project.project_title}")
        print(f"  * Status: {dict(Project.ProjectStatus.choices).get(project.project_status)}")
        print(f"  * Intent Form Submitted: True")
        print(f"  * Intent Form Approved: False\n")
        
        print(f"{Colors.YELLOW}View at:{Colors.END}")
        print(f"  * http://127.0.0.1:8000/admin/intent/submitted/\n")
        
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR] {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
