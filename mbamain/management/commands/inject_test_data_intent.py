from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mbamain.models import StudentProfile, Project

User = get_user_model()

class Command(BaseCommand):
    help = "Create intent form test data - Tobey Mbatoa with submitted intent form"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Delete existing Tobey Mbatoa test data before creating new one',
        )

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write("  INTENT FORM TEST DATA INJECTION".center(80))
        self.stdout.write("="*80 + "\n")

        email = "tobey.mbatoa@test.mba.local"
        
        if options['clean']:
            self.stdout.write("Cleaning up old test data...")
            try:
                old_user = User.objects.get(email=email)
                Project.objects.filter(student=old_user).delete()
                old_user.delete()
                self.stdout.write(self.style.SUCCESS("[OK] Old user cleaned\n"))
            except User.DoesNotExist:
                self.stdout.write(self.style.SUCCESS("[OK] No old data found\n"))
        
        try:
            # Create or get student user
            user, created = User.objects.get_or_create(
                username=email,  # Changed: use email as username for login
                defaults={
                    'email': email,
                    'user_type': User.UserType.STUDENT,
                }
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created student: {user.email}\n"))
            else:
                self.stdout.write(self.style.WARNING(f"Student already exists: {user.email}\n"))
            
            # Create or update student profile
            StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'name': 'Tobey',
                    'surname': 'Mbatoa',
                    'title': 'Mr.',
                    'student_no': 'STU99999',
                    'contact': '+1-555-9999',
                    'module': 'MBA',
                    'block_id': 'BLOCK_TEST',
                    'degree': 'MBA',
                    'address': '123 Intent Street, Test University'
                }
            )
            
            # Create or update project with intent form submitted
            project, created = Project.objects.get_or_create(
                student=user,
                defaults={
                    'project_title': 'Advanced Research in Business Intelligence and Analytics',
                    'project_description': 'A comprehensive study of business intelligence systems.',
                    'discipline': 'Business Analytics, Finance',
                    'project_status': Project.ProjectStatus.Notice_submitted,
                    'qualification': 'MBA',
                    'sdg_goal': 'Goal 8: Decent Work and Economic Growth',
                    'intent_form_submitted': True,
                    'intent_form_approved': False
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS("Created project with intent form\n"))
            else:
                self.stdout.write(self.style.WARNING("Project already exists\n"))
            
            # Print summary
            self.stdout.write("="*80)
            self.stdout.write("  INJECTION COMPLETE".center(80))
            self.stdout.write("="*80 + "\n")
            
            self.stdout.write(self.style.WARNING("Test Data:"))
            self.stdout.write(f"  * Student Name: Tobey Mbatoa")
            self.stdout.write(f"  * Email: {email}")
            self.stdout.write(f"  * Username: {email}")  # Changed: show email as username
            self.stdout.write(f"  * Password: testpass123")
            self.stdout.write(f"  * Student Number: STU99999")
            self.stdout.write(f"  * Project: {project.project_title}")
            self.stdout.write(f"  * Intent Form Submitted: True\n")
            self.stdout.write("="*80 + "\n")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[ERROR] {str(e)}"))
            import traceback
            traceback.print_exc()
