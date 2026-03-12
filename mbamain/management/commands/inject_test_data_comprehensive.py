from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import datetime
from mbamain.models import StudentProfile, SupervisorProfile, Project, Invite

User = get_user_model()

class Command(BaseCommand):
    help = "Create comprehensive test data: 5 supervisors + 15 students with projects"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Delete existing test data before creating new ones',
        )

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*90)
        self.stdout.write("  COMPREHENSIVE TEST DATA INJECTION".center(90))
        self.stdout.write("="*90 + "\n")

        if options['clean']:
            self.cleanup_old_data()

        supervisors = self.create_supervisors(5)
        students, projects = self.create_students(15, supervisors)
        self.print_summary(supervisors, students)

    def cleanup_old_data(self):
        """Remove old test data to avoid conflicts"""
        self.stdout.write("Cleaning up old test data...")
        try:
            Invite.objects.filter(project__student__username__startswith='inject_test_student').delete()
            Project.objects.filter(student__username__startswith='inject_test_student').delete()
            User.objects.filter(username__startswith='inject_test_student').delete()
            User.objects.filter(username__startswith='inject_test_supervisor').delete()
            self.stdout.write(self.style.SUCCESS("[OK] Old test data cleaned"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[FAIL] Cleanup error: {str(e)}"))

    def create_supervisors(self, count=5):
        """Create test supervisors with skill profiles"""
        self.stdout.write(f"\nCreating {count} supervisors...")
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
            
            if User.objects.filter(username=username).exists():
                self.stdout.write(f"  → Supervisor {i+1} already exists")
                supervisors.append(User.objects.get(username=username))
                continue
            
            try:
                user = User.objects.create_user(
                    username=email,  # Changed: use email as username for login
                    email=email,
                    password='testpass123',
                    user_type=User.UserType.SCHOLAR,
                )
                
                fname, lname = names[i % len(names)]
                SupervisorProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'name': fname,
                        'surname': lname,
                        'title': ['Prof.', 'Dr.', 'Ms.', 'Mr.'][i % 4],
                        'skills': skills_list[i % len(skills_list)],
                        'department': ['Business School', 'Engineering', 'Science', 'Law'][i % 4],
                        'position': ['Lecturer', 'Senior Lecturer', 'Associate Professor'][i % 3],
                        'contact': f"+1-555-{1000+i:04d}",
                        'students': i
                    }
                )
                
                supervisors.append(user)
                self.stdout.write(f"  {self.style.SUCCESS('[OK]')} Supervisor {i+1}: {user.email}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  [FAIL] {str(e)}"))
        
        return supervisors

    def create_students(self, count=15, supervisors=None):
        """Create test students with projects at different workflow stages"""
        self.stdout.write(f"\nCreating {count} students with projects...")
        
        disciplines = ['Machine Learning', 'Cloud Computing', 'Cybersecurity', 'Business Analytics', 'Digital Marketing']
        statuses = [
            Project.ProjectStatus.CREATED,
            Project.ProjectStatus.HDC_SUBMITTED,
            Project.ProjectStatus.JBS5_submitted,
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
            
            if User.objects.filter(username=username).exists():
                self.stdout.write(f"  → Student {i+1} already exists")
                students.append(User.objects.get(username=username))
                continue
            
            try:
                user = User.objects.create_user(
                    username=email,  # Changed: use email as username for login
                    email=email,
                    password='testpass123',
                    user_type=User.UserType.STUDENT,
                )
                
                fname, lname = names[i % len(names)]
                StudentProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'name': fname,
                        'surname': lname,
                        'title': ['Mr.', 'Ms.', 'Mrs.'][i % 3],
                        'student_no': f"STU{i+1:05d}",
                        'contact': f"+1-555-{2000+i:04d}",
                        'module': 'MBA',
                        'block_id': f"BLOCK_{chr(65 + (i % 5))}",
                        'degree': 'MBA',
                        'address': f"{i+1} Academic Street, University City"
                    }
                )
                
                project_status = statuses[i % len(statuses)]
                project = Project.objects.create(
                    student=user,
                    project_title=f"Research on {disciplines[i % len(disciplines)]} - Phase {(i % 3) + 1}",
                    project_description=f"Comprehensive research into {disciplines[i % len(disciplines)]}.",
                    discipline=disciplines[i % len(disciplines)],
                    project_status=project_status,
                    qualification='MBA',
                    sdg_goal='Goal 8: Decent Work and Economic Growth'
                )
                
                if project_status != Project.ProjectStatus.CREATED and supervisors:
                    supervisor = supervisors[i % len(supervisors)]
                    project.primary_supervisor = supervisor.id
                    Invite.objects.create(
                        user=supervisor,
                        project=project,
                        invite_type=False,
                        response=True if project_status != Project.ProjectStatus.HDC_SUBMITTED else None,
                        read=True
                    )
                
                project.save()
                students.append(user)
                projects.append(project)
                
                status_name = dict(Project.ProjectStatus.choices).get(project_status, 'Unknown')
                self.stdout.write(f"  {self.style.SUCCESS('[OK]')} Student {i+1}: {user.email} | Status: {status_name}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  [FAIL] {str(e)}"))
        
        return students, projects

    def print_summary(self, supervisors, students):
        """Print summary of created data"""
        self.stdout.write("\n" + "="*90)
        self.stdout.write("  TEST DATA INJECTION SUMMARY".center(90))
        self.stdout.write("="*90 + "\n")
        
        self.stdout.write(self.style.SUCCESS("Created Records:"))
        self.stdout.write(f"  * Supervisors: {len(supervisors)}")
        self.stdout.write(f"  * Students: {len(students)}")
        
        projects = Project.objects.filter(student__username__startswith='inject_test_student')
        self.stdout.write(f"  * Projects: {projects.count()}")
        
        self.stdout.write(self.style.WARNING("\nProject Status Breakdown:"))
        status_counts = {}
        for project in projects:
            status_name = dict(Project.ProjectStatus.choices).get(project.project_status)
            status_counts[status_name] = status_counts.get(status_name, 0) + 1
        
        for status, count in sorted(status_counts.items()):
            self.stdout.write(f"  * {status}: {count}")
        
        self.stdout.write(self.style.WARNING("\nTest Credentials:"))
        for i in range(1, 6):
            self.stdout.write(f"  Supervisor {i}: inject_test_supervisor_{i}@test.mba.local / testpass123")
        self.stdout.write("")
        for i in range(1, 6):
            self.stdout.write(f"  Student {i}: inject_test_student_{i}@test.mba.local / testpass123")
        
        self.stdout.write("\n" + "="*90 + "\n")
