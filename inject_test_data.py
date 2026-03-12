#!/usr/bin/env python
"""
Test Data Injection Script
Creates complete test data with supervisors, students, and projects at different workflow stages
Usage: python inject_test_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import get_user_model
from mbamain.models import (
    StudentProfile, SupervisorProfile, Project, Invite
)

User = get_user_model()

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def cleanup_old_data():
    """Remove old test data to avoid conflicts"""
    print(f"\n{Colors.YELLOW}Cleaning up old test data...{Colors.END}")
    try:
        # Delete in order of dependencies
        Invite.objects.filter(project__student__username__startswith='inject_test_student').delete()
        Project.objects.filter(student__username__startswith='inject_test_student').delete()
        User.objects.filter(username__startswith='inject_test_student').delete()
        User.objects.filter(username__startswith='inject_test_supervisor').delete()
        print(f"{Colors.GREEN}[OK] Old test data cleaned{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[FAIL] Cleanup error: {str(e)}{Colors.END}")

def create_supervisors(count=5):
    """Create test supervisors with skill profiles"""
    print(f"\n{Colors.BLUE}Creating {count} supervisors...{Colors.END}")
    supervisors = []
    skills_list = [
        "Machine Learning, Data Science",
        "Cloud Computing, DevOps",
        "Cybersecurity, Network Architecture",
        "Business Analytics, Finance",
        "Digital Marketing, Brand Strategy"
    ]
    
    names = [
        ('James', 'Smith'), ('Maria', 'Johnson'), ('Robert', 'Williams'),
        ('Patricia', 'Brown'), ('Michael', 'Jones')
    ]
    
    for i in range(count):
        username = f"inject_test_supervisor_{i+1}"
        email = f"supervisor_{i+1}@test.mba.local"
        
        # Check if already exists
        if User.objects.filter(username=username).exists():
            print(f"  -> Supervisor {i+1} already exists")
            supervisors.append(User.objects.get(username=username))
            continue
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password='testpass123',
                user_type=User.UserType.SCHOLAR,
                is_staff=False,
                has_profile=True
            )
            
            fname, lname = names[i % len(names)]
            
            # Create supervisor profile
            SupervisorProfile.objects.create(
                user=user,
                name=fname,
                surname=lname,
                title=['Prof.', 'Dr.', 'Ms.', 'Mr.'][i % 4],
                skills=skills_list[i % len(skills_list)],
                department=['Business School', 'Engineering', 'Science', 'Law'][i % 4],
                position=['Lecturer', 'Senior Lecturer', 'Associate Professor'][i % 3],
                contact=f"+1-555-{1000+i:04d}",
                students=i
            )
            
            supervisors.append(user)
            print(f"  {Colors.GREEN}[OK]{Colors.END} Supervisor {i+1}: {user.email} | Skills: {skills_list[i % len(skills_list)]}")
        except Exception as e:
            print(f"  {Colors.RED}[FAIL]{Colors.END} Failed to create supervisor: {str(e)}")
    
    return supervisors

def create_students(count=15, supervisors=None):
    """Create test students with projects at different workflow stages"""
    print(f"\n{Colors.BLUE}Creating {count} students with projects...{Colors.END}")
    
    disciplines = ['Machine Learning', 'Cloud Computing', 'Cybersecurity', 'Business Analytics', 'Digital Marketing']
    statuses = [
        Project.ProjectStatus.CREATED,  # New, no supervisor
        Project.ProjectStatus.HDC_SUBMITTED,  # Supervisor assigned
        Project.ProjectStatus.JBS5_submitted,  # Form submitted
    ]
    
    names = [
        ('Alex', 'Anderson'), ('Sarah', 'Blake'), ('Chris', 'Carter'),
        ('Emma', 'Davis'), ('David', 'Evans'), ('Olivia', 'Fisher'),
        ('Frank', 'Garcia'), ('Grace', 'Harris'), ('Henry', 'Iverson'),
        ('Iris', 'Jenkins'), ('Jack', 'Kim'), ('Julia', 'Lopez'),
        ('Kevin', 'Martinez'), ('Laura', 'Nelson'), ('Mark', 'O\'Brien')
    ]
    
    students = []
    projects = []
    
    for i in range(count):
        username = f"inject_test_student_{i+1}"
        email = f"student_{i+1}@test.mba.local"
        
        # Check if already exists
        if User.objects.filter(username=username).exists():
            print(f"  -> Student {i+1} already exists")
            students.append(User.objects.get(username=username))
            continue
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password='testpass123',
                user_type=User.UserType.STUDENT,
                is_staff=False,
                has_profile=True
            )
            
            fname, lname = names[i % len(names)]
            
            # Create student profile
            StudentProfile.objects.create(
                user=user,
                name=fname,
                surname=lname,
                title=['Mr.', 'Ms.', 'Mrs.'][i % 3],
                student_no=f"STU{i+1:05d}",
                contact=f"+1-555-{2000+i:04d}",
                module='MBA',
                block_id=f"BLOCK_{chr(65 + (i % 5))}",
                degree='MBA',
                address=f"{i+1} Academic Street, University City"
            )
            
            # Create project
            project_status = statuses[i % len(statuses)]
            project = Project.objects.create(
                student=user,
                project_title=f"Research on {disciplines[i % len(disciplines)]} - Phase {(i % 3) + 1}",
                project_description=f"Comprehensive research into {disciplines[i % len(disciplines)]} technologies and their business applications.",
                discipline=disciplines[i % len(disciplines)],
                project_status=project_status,
                qualification='MBA',
                sdg_goal='Goal 8: Decent Work and Economic Growth'
            )
            
            # Assign supervisor for projects that aren't CREATED
            if project_status != Project.ProjectStatus.CREATED and supervisors:
                supervisor = supervisors[i % len(supervisors)]
                project.primary_supervisor = supervisor.id
                
                # Create invite
                Invite.objects.create(
                    user=supervisor,
                    project=project,
                    invite_type=False,  # Supervisor invite
                    response=True if project_status != Project.ProjectStatus.HDC_SUBMITTED else None,
                    read=True
                )
            
            project.save()
            students.append(user)
            projects.append(project)
            
            status_name = dict(Project.ProjectStatus.choices).get(project_status, 'Unknown')
            if project_status != Project.ProjectStatus.CREATED and supervisors:
                supervisor_info = f" [Supervisor: {supervisors[i % len(supervisors)].email}]"
            else:
                supervisor_info = ""
            print(f"  {Colors.GREEN}[OK]{Colors.END} Student {i+1}: {user.email} | Status: {status_name}{supervisor_info}")
            
        except Exception as e:
            print(f"  {Colors.RED}[FAIL]{Colors.END} Failed to create student: {str(e)}")
    
    return students, projects

def print_summary(supervisors, students):
    """Print summary of created data"""
    print(f"\n{Colors.BLUE}{'='*90}{Colors.END}")
    print(f"{Colors.BLUE}{'TEST DATA INJECTION SUMMARY':^90}{Colors.END}")
    print(f"{Colors.BLUE}{'='*90}{Colors.END}\n")
    
    print(f"{Colors.GREEN}Created Records:{Colors.END}")
    print(f"  * Supervisors: {len(supervisors)}")
    print(f"  * Students: {len(students)}")
    
    projects = Project.objects.filter(student__username__startswith='inject_test_student')
    print(f"  * Projects: {projects.count()}")
    
    status_counts = {}
    for project in projects:
        status_name = dict(Project.ProjectStatus.choices).get(project.project_status, 'Unknown')
        status_counts[status_name] = status_counts.get(status_name, 0) + 1
    
    print(f"\n{Colors.BLUE}Project Status Breakdown:{Colors.END}")
    for status, count in sorted(status_counts.items()):
        print(f"  * {status}: {count}")
    
    print(f"\n{Colors.YELLOW}Access Test Data At:{Colors.END}")
    print(f"  * http://127.0.0.1:8000/admin/                 (Admin Dashboard)")
    print(f"  * http://127.0.0.1:8000/admin/manage/          (Manage Students)")
    print(f"  * http://127.0.0.1:8000/                       (Student Login)")
    
    print(f"\n{Colors.YELLOW}Test Credentials (15 students + 5 supervisors):{Colors.END}")
    for i in range(1, 6):
        print(f"  * Supervisor {i}: inject_test_supervisor_{i}@test.mba.local / testpass123")
    print()
    for i in range(1, 6):
        print(f"  * Student {i}: inject_test_student_{i}@test.mba.local / testpass123")
    
    print(f"\n{Colors.BLUE}{'='*90}{Colors.END}\n")

def main():
    """Main execution"""
    print(f"\n{Colors.BLUE}{'='*90}{Colors.END}")
    print(f"{Colors.BLUE}{'TEST DATA INJECTION SCRIPT':^90}{Colors.END}")
    print(f"{Colors.BLUE}{'Injects supervisors, students, and projects at various workflow stages':^90}{Colors.END}")
    print(f"{Colors.BLUE}{'='*90}{Colors.END}")
    
    # Cleanup
    cleanup_old_data()
    
    # Create supervisors
    supervisors = create_supervisors(5)
    
    # Create students and projects
    students, projects = create_students(15, supervisors)
    
    # Print summary
    print_summary(supervisors, students)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INTERRUPTED] Injection cancelled by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()
