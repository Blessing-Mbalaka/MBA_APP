from django.core.management.base import BaseCommand
from mbamain.models import AUser


class Command(BaseCommand):
    help = "Create test users for workflow testing with known credentials"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Delete existing test users before creating new ones',
        )

    def handle(self, *args, **kwargs):
        if kwargs['clean']:
            # Delete old test users created with wrong usernames
            old_users = ['mainAdmin', 'admin', 'hdc', 'scholar', 'student', 'examiner']
            for username in old_users:
                try:
                    user = AUser.objects.get(username=username)
                    user.delete()
                    self.stdout.write(f"[DELETED] {username}")
                except AUser.DoesNotExist:
                    pass
        
        self.stdout.write("\n" + "="*80)
        self.stdout.write("  CREATING TEST USERS FOR WORKFLOW TESTING")
        self.stdout.write("="*80 + "\n")

        # Note: username should be the email for login to work
        # The signin view does: authenticate(request, username=email, password=password)
        test_users = [
            ('mainAdmin@test.com', 'mainAdmin@test.com', 'mainAdmin@123', AUser.UserType.MAIN_ADMIN, 'Main', 'Admin'),
            ('admin@test.com', 'admin@test.com', 'admin@123', AUser.UserType.ADMIN, 'Admin', 'User'),
            ('hdc@test.com', 'hdc@test.com', 'hdc@123', AUser.UserType.HDC, 'HDC', 'User'),
            ('scholar@test.com', 'scholar@test.com', 'scholar@123', AUser.UserType.SCHOLAR, 'Scholar', 'Supervisor'),
            ('student@test.com', 'student@test.com', 'student@123', AUser.UserType.STUDENT, 'Student', 'User'),
            ('examiner@test.com', 'examiner@test.com', 'examiner@123', AUser.UserType.EXAMINER, 'Examiner', 'User'),
        ]

        created = 0
        existing = 0

        for username, email, password, user_type, first_name, last_name in test_users:
            try:
                user = AUser.objects.get(username=username)
                self.stdout.write(f"[EXISTS] {email}")
                existing += 1
            except AUser.DoesNotExist:
                user = AUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    user_type=user_type,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=True,
                )
                self.stdout.write(f"[CREATED] {email}")
                created += 1

        # Print credentials table
        self.stdout.write("\n" + "="*80)
        self.stdout.write("  TEST USER CREDENTIALS (Use Email for Login)")
        self.stdout.write("="*80)
        self.stdout.write("\nEmail                    | Password      | User Type")
        self.stdout.write("-" * 70)

        for username, email, password, user_type, _, _ in test_users:
            user_type_map = {
                0: "MAIN_ADMIN",
                1: "ADMIN",
                2: "SCHOLAR",
                3: "STUDENT",
                4: "EXAMINER",
                5: "HDC",
            }
            user_type_name = user_type_map.get(user_type, "UNKNOWN")
            self.stdout.write(
                f"{email:<24} | {password:<13} | {user_type_name}"
            )

        self.stdout.write("-" * 70)
        self.stdout.write(f"\nCreated: {created} | Existing: {existing}")
        self.stdout.write("\n" + "="*80 + "\n")
