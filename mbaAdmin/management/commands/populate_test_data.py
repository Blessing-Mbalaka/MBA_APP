from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mbamain.models import Project, Invite, StudentProfile, SupervisorProfile, JBS5, JBS10, StudentSupervisorForm, NoticeToSubmitForm, NominationForm
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = "Populate test data for page loading tests"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Delete existing test data before creating new data',
        )

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write("  TEST DATA POPULATION")
        self.stdout.write("="*80 + "\n")

        if options['clean']:
            self.clean_test_data()

        # Create test users with correct user types:
        # STUDENT = 3, SCHOLAR = 2, EXAMINER = 4
        student = self.create_user('test_student', 'student@test.com', 3, 'Test', 'Student')
        scholar = self.create_user('test_scholar', 'scholar@test.com', 2, 'Test', 'Scholar')
        examiner = self.create_user('test_examiner', 'examiner@test.com', 4, 'Test', 'Examiner')

        # Create profiles
        student_profile, created = StudentProfile.objects.get_or_create(
            user=student,
            defaults={
                'name': 'Test',
                'surname': 'Student',
                'student_no': 'TS001',
                'contact': '0123456789',
                'block_id': 'BLOCK001',
                'created_at': datetime.now(),
            }
        )
        if created:
            self.stdout.write("[CREATED] Student profile")
        else:
            self.stdout.write("[EXISTS] Student profile")

        supervisor_profile, created = SupervisorProfile.objects.get_or_create(
            user=scholar,
            defaults={
                'name': 'Test',
                'surname': 'Scholar',
                'contact': '0987654321',
                'created_at': datetime.now(),
            }
        )
        if created:
            self.stdout.write("[CREATED] Supervisor profile")
        else:
            self.stdout.write("[EXISTS] Supervisor profile")

        # Create projects
        project_count = 0
        for i in range(5):
            project, created = Project.objects.get_or_create(
                project_title=f'Test Project {i+1}',
                student=student,
                defaults={
                    'project_description': f'This is a test project {i+1}',
                    'project_start_date': datetime.now().date(),
                    'created_date': datetime.now(),
                    'project_status': 0,
                    'discipline': 'Computer Science',
                }
            )
            if created:
                project_count += 1
        self.stdout.write(f"[CREATED] {project_count} test projects")

        # Create invites for projects
        projects = Project.objects.filter(student=student)[:5]
        invite_count = 0
        for i, project in enumerate(projects):
            invite, created = Invite.objects.get_or_create(
                user=examiner,
                project=project,
                defaults={
                    'invite_type': False,
                    'read': False,
                    'response': False,
                    'created_at': datetime.now(),
                    'count': i + 1,
                }
            )
            if created:
                invite_count += 1
        self.stdout.write(f"[CREATED] {invite_count} project invites")

        # Create scholar invites
        scholar_invite_count = 0
        for i in range(3):
            invite, created = Invite.objects.get_or_create(
                user=scholar,
                defaults={
                    'invite_type': True,
                    'read': False,
                    'response': False,
                    'created_at': datetime.now(),
                    'count': i + 1,
                }
            )
            if created:
                scholar_invite_count += 1
        self.stdout.write(f"[CREATED] {scholar_invite_count} scholar invites")

        # Create form records for the first project
        first_project = Project.objects.filter(student=student).first()
        if first_project:
            # Create JBS5
            jbs5, created = JBS5.objects.get_or_create(
                project=first_project,
                defaults={
                    'study_type': 'Research',
                    'ir': 'IR Research',
                    'qualification': 'MBA',
                    'title': 'Test Research Project',
                    'research_specific': True,
                    'secondary_focus': False,
                    'registration_date': datetime.now().date(),
                    'student_signed': False,
                    'supervisor_signed': False,
                }
            )
            self.stdout.write("[CREATED] JBS5 form" if created else "[EXISTS] JBS5 form")

            # Create JBS10
            jbs10, created = JBS10.objects.get_or_create(
                project=first_project,
                defaults={
                    'is_uj_staff': False,
                    'capstone_project': 'dissertation',
                    'proposed_title': 'Test Research Project',
                    'is_4ir_research': False,
                }
            )
            self.stdout.write("[CREATED] JBS10 form" if created else "[EXISTS] JBS10 form")

            # Create StudentSupervisorForm
            sp_form, created = StudentSupervisorForm.objects.get_or_create(
                project=first_project,
                defaults={
                    'initials_student': 'TS',
                    'initials_supervisor': 'TS',
                    'supervisor_signed': False,
                    'student_signed': False,
                }
            )
            self.stdout.write("[CREATED] StudentSupervisorForm" if created else "[EXISTS] StudentSupervisorForm")

            # Create NoticeToSubmitForm (no signature required initially)
            notice_form, created = NoticeToSubmitForm.objects.get_or_create(
                project=first_project,
                defaults={
                    'auth_student': 'Test Student',
                    'supervisor_agree': False,
                    'approved_hdc': False,
                    'title_approved_hdc': False,
                    'nominated_examinners': False,
                }
            )
            self.stdout.write("[CREATED] NoticeToSubmitForm" if created else "[EXISTS] NoticeToSubmitForm")

            # Create NominationForm
            nomination_form, created = NominationForm.objects.get_or_create(
                project=first_project,
                defaults={
                    'degree': 'MBA',
                    'qualification': 'MBA',
                    'supervisor_signed': False,
                }
            )
            self.stdout.write("[CREATED] NominationForm" if created else "[EXISTS] NominationForm")

        self.stdout.write("\n" + "="*80)
        self.stdout.write("  TEST DATA POPULATION COMPLETE")
        self.stdout.write("  Now run: python manage.py test_page_loading")
        self.stdout.write("="*80 + "\n")

    def create_user(self, username, email, user_type, first_name='', last_name=''):
        """Create a user if it doesn't exist"""
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"[EXISTS] User: {username}")
            return user
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=email,
                password='testpass123',
                user_type=user_type,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )
            self.stdout.write(f"[CREATED] User: {username}")
            return user

    def clean_test_data(self):
        """Delete test data"""
        self.stdout.write("[CLEANING] Removing test data...\n")
        
        # Delete form records first
        JBS5.objects.filter(project__student__username__startswith='test_').delete()
        JBS10.objects.filter(project__student__username__startswith='test_').delete()
        StudentSupervisorForm.objects.filter(project__student__username__startswith='test_').delete()
        NoticeToSubmitForm.objects.filter(project__student__username__startswith='test_').delete()
        NominationForm.objects.filter(project__student__username__startswith='test_').delete()
        self.stdout.write("[DELETED] Test forms")
        
        # Delete invites (has foreign keys to projects/users)
        Invite.objects.filter(user__username__startswith='test_').delete()
        self.stdout.write("[DELETED] Test invites")
        
        # Delete projects (has foreign key to student user)
        Project.objects.filter(student__username__startswith='test_').delete()
        self.stdout.write("[DELETED] Test projects")
        
        # Delete student/supervisor profiles
        StudentProfile.objects.filter(user__username__startswith='test_').delete()
        SupervisorProfile.objects.filter(user__username__startswith='test_').delete()
        self.stdout.write("[DELETED] Test profiles")
        
        # Finally delete test users
        test_users = User.objects.filter(username__startswith='test_')
        count = test_users.count()
        test_users.delete()
        self.stdout.write(f"[DELETED] {count} test users\n")
