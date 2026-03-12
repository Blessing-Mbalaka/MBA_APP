from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from mbamain.models import Project, NominationForm

User = get_user_model()

class Command(BaseCommand):
    help = "Create nomination form test data for test students"

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write("  NOMINATION FORM TEST DATA INJECTION".center(80))
        self.stdout.write("="*80 + "\n")

        # Get existing test students
        test_students = User.objects.filter(username__startswith='inject_test_student_')[:5]

        if not test_students.exists():
            self.stdout.write(self.style.WARNING("No test students found! Run inject_test_data_comprehensive first."))
            return

        # Get first supervisor for projects
        supervisors = User.objects.filter(username__startswith='inject_test_supervisor_')
        if not supervisors.exists():
            self.stdout.write(self.style.WARNING("No test supervisors found! Run inject_test_data_comprehensive first."))
            return

        supervisor = supervisors.first()

        self.stdout.write(self.style.SUCCESS(f"Found {test_students.count()} test students"))
        self.stdout.write(self.style.SUCCESS(f"Found {supervisors.count()} test supervisors\n"))

        created_count = 0
        updated_count = 0
        
        for student in test_students:
            project, created = Project.objects.get_or_create(
                student=student,
                defaults={
                    'project_title': f'Research Nomination Test Project for {student.first_name}',
                    'project_description': f'Test project for nomination - {student.username}',
                    'primary_supervisor': supervisor.id,
                    'discipline': 'Machine Learning',
                    'nomination_form_submitted': True,
                    'created_date': timezone.now(),
                }
            )
            
            # Ensure nomination_form_submitted is True
            if not project.nomination_form_submitted:
                project.nomination_form_submitted = True
                project.save()
                updated_count += 1
                self.stdout.write(f"  → Updated project for {student.username}")
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"  [OK] Created project for {student.username}"))
                created_count += 1
            
            # Create NominationForm
            nomination_form, form_created = NominationForm.objects.get_or_create(
                project=project,
                defaults={
                    'co_supervisor_full_names': f'Dr. Test Co-Supervisor for {student.first_name}',
                    'co_supervisor_department': 'Engineering',
                    'co_supervisor_phone': '+27123456789',
                    'co_supervisor_email': f'cosupervisor_{student.username}@university.ac.za',
                    'degree': 'MEng (Coursework)',
                    'qualification': 'PhD, MSc',
                    'supervisor_signed': True,
                }
            )
            
            if form_created:
                self.stdout.write(f"  → Created nomination form for {student.username}")

        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.SUCCESS("  NOMINATION TEST DATA COMPLETE".center(80)))
        self.stdout.write("="*80)
        self.stdout.write(f"\n  New projects created: {created_count}")
        self.stdout.write(f"  Existing projects updated: {updated_count}")
        self.stdout.write("\n" + "="*80 + "\n")
