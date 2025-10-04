from django.core.management.base import BaseCommand
from mbamain.models import ResearchInterest


class Command(BaseCommand):
    help = "Load predefined research interests into the database"

    def handle(self, *args, **kwargs):
        interests = [
            'Leadership', 'Business', 'Economics', 'Maths', 'Researcher', 'Agriculture',
            'Entrepreneurship', 'Project Management', 'HR', 'Organisational Behavior',
            'HSE', 'Change Management', 'Psychology', 'Education', 'Management', 'Strategy',
            'Marketing', 'Supply Chain', 'Finance', 'Hospitality', 'Human Capital Development',
            'Governance', 'SME', 'Strategic Management', 'Technology'
        ]

        created_count = 0
        skipped_count = 0

        for interest in interests:
            obj, created = ResearchInterest.objects.get_or_create(
                name=interest,
                defaults={"created_by": "management_command"}
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f" {created_count} new interests added, {skipped_count} already existed."
        ))
