from django.core.management.base import BaseCommand
from mbamain.models import ResearchInterest


class Command(BaseCommand):
    help = 'Populate ResearchInterest table with default discipline categories'
    
    DISCIPLINES = {
        'Computer Science': 'Core IT and computer science disciplines',
        'Business Management': 'General business and management studies',
        'Finance & Banking': 'Finance, banking, and accounting disciplines',
        'Engineering': 'Engineering and technical disciplines',
        'Healthcare': 'Medical, healthcare, and nursing disciplines',
        'Education': 'Educational studies and pedagogy',
        'Agriculture': 'Agricultural and environmental sciences',
        'Environmental Science': 'Environmental and sustainability studies',
        'Law & Governance': 'Law, political science, and governance',
        'Psychology': 'Psychology and behavioral sciences',
        'Economics': 'Economic studies and econometrics',
        'Marketing': 'Marketing and brand management',
        'Human Resources': 'HR management and organizational behavior',
        'Operations Management': 'Operations and process management',
        'Supply Chain Management': 'Supply chain and logistics management',
        'Information Technology': 'IT systems and technology management',
        'Data Science': 'Data science and analytics',
        'Artificial Intelligence': 'AI and machine learning',
        'Cybersecurity': 'Cybersecurity and information security',
        'Public Administration': 'Public policy and administration',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing ResearchInterest entries before populating',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all current ResearchInterest entries',
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_disciplines()
            return

        if options['clear']:
            ResearchInterest.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all ResearchInterest entries'))

        created_count = 0
        for name in self.DISCIPLINES.keys():
            obj, created = ResearchInterest.objects.get_or_create(name=name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {name}'))
            else:
                self.stdout.write(f'✓ Already exists: {name}')

        total_count = ResearchInterest.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Complete! {created_count} new disciplines created. Total disciplines: {total_count}'
            )
        )

    def list_disciplines(self):
        disciplines = ResearchInterest.objects.all().order_by('name')
        if not disciplines.exists():
            self.stdout.write(self.style.WARNING('No disciplines found in database'))
            return

        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('Current ResearchInterest Disciplines:')
        self.stdout.write('=' * 50)
        for i, discipline in enumerate(disciplines, 1):
            self.stdout.write(f'{i:2d}. {discipline.name}')
        self.stdout.write('=' * 50 + '\n')
