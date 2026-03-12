from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import get_resolver
from django.urls import URLPattern, URLResolver
from colorama import Fore, Back, Style, init
from datetime import datetime
from mbamain.models import Project, Invite, StudentProfile, AUser
import os
import sys
import io

# Set stdout encoding to UTF-8 for Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class Command(BaseCommand):
    help = "Test all URL endpoints for page loading and 404 errors"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_pages = []
        self.passed_pages = []
        self.skipped_pages = []

    def add_arguments(self, parser):
        parser.add_argument(
            '--log-file',
            type=str,
            default='logs.txt',
            help='Path to log file for failed pages (default: logs.txt)',
        )

    def get_all_urls(self, urlpatterns, prefix=''):
        """Recursively extract all URL patterns"""
        urls = []
        for pattern in urlpatterns:
            if isinstance(pattern, URLResolver):
                # This is a nested URL configuration
                new_prefix = prefix + str(pattern.pattern)
                urls.extend(self.get_all_urls(pattern.url_patterns, new_prefix))
            elif isinstance(pattern, URLPattern):
                # This is an actual URL pattern
                full_pattern = prefix + str(pattern.pattern)
                urls.append({
                    'pattern': full_pattern,
                    'name': pattern.name,
                })
        return urls

    def extract_url_path(self, pattern, test_data=None):
        """Convert URL pattern to testable path"""
        import re
        path = str(pattern)
        
        # Default test data values
        if test_data is None:
            test_data = {'project_id': '1', 'invite_id': '1', 'user_id': '1', 'id': '1', 'assessor_id': '1'}
        
        # Replace parameterized URL parts with test values
        # Handle <int:xyz>, <str:xyz>, <uuid:xyz>, etc.
        path = re.sub(r'<int:(\w+)>', lambda m: str(test_data.get(m.group(1), '1')), path)
        # For str parameters, check if they look like IDs - use actual data, otherwise use test
        path = re.sub(r'<str:(id|project_id|user_id|invite_id|assessor_id)>', lambda m: str(test_data.get(m.group(1), '1')), path)
        path = re.sub(r'<str:\w+>', 'test', path)
        path = re.sub(r'<uuid:\w+>', '550e8400-e29b-41d4-a716-446655440000', path)
        path = re.sub(r'<slug:\w+>', 'test-slug', path)
        
        # Fallback for any remaining angle brackets
        path = re.sub(r'<[^>]+>', str(test_data.get('id', '1')), path)
        
        path = '/' + path if not path.startswith('/') else path
        return path

    def test_url(self, client, path, url_name):
        """Test a single URL"""
        try:
            response = client.get(path, follow=True)
            
            if response.status_code == 404:
                return False, response.status_code, "Page not found (404)"
            elif response.status_code >= 500:
                return False, response.status_code, f"Server error ({response.status_code})"
            elif response.status_code in [200, 301, 302, 403]:
                return True, response.status_code, "OK"
            else:
                return False, response.status_code, f"Unexpected status ({response.status_code})"
        except Exception as e:
            return False, None, str(e)

    def handle(self, *args, **options):
        log_file = options['log_file']
        
        self.stdout.write(
            f"\n{Back.CYAN}{Fore.BLACK}{'='*80}{Style.RESET_ALL}"
        )
        self.stdout.write(
            f"{Back.CYAN}{Fore.BLACK}  PAGE LOADING TEST SUITE{Style.RESET_ALL}"
        )
        self.stdout.write(
            f"{Back.CYAN}{Fore.BLACK}{'='*80}{Style.RESET_ALL}\n"
        )
        
        # Get all URL patterns
        resolver = get_resolver()
        all_urls = self.get_all_urls(resolver.url_patterns)
        
        self.stdout.write(
            f"{Fore.YELLOW}Found {len(all_urls)} URL patterns{Style.RESET_ALL}\n"
        )
        
        # Look up actual test data IDs from the database
        test_data = {'project_id': '1', 'invite_id': '1', 'user_id': '1', 'id': '1', 'assessor_id': '1'}
        try:
            first_project = Project.objects.filter(student__username__startswith='test_').first()
            if first_project:
                test_data['project_id'] = str(first_project.id)
                test_data['id'] = str(first_project.id)
            
            first_invite = Invite.objects.filter(user__username__startswith='test_').first()
            if first_invite:
                test_data['invite_id'] = str(first_invite.id)
            
            first_user = AUser.objects.filter(username__startswith='test_').first()
            if first_user:
                test_data['user_id'] = str(first_user.id)
                test_data['assessor_id'] = str(first_user.id)
        except Exception as e:
            self.stdout.write(
                f"{Fore.YELLOW}[INFO] Could not load test data from database: {e}{Style.RESET_ALL}\n"
            )
        
        # Create Django test client
        client = Client()
        
        self.stdout.write(f"{Fore.CYAN}Testing URLs...{Style.RESET_ALL}\n")
        
        # Test each URL
        for url_info in all_urls:
            pattern = url_info['pattern']
            name = url_info['name'] or 'unnamed'
            
            path = self.extract_url_path(pattern, test_data)
            
            # Test the URL
            success, status_code, message = self.test_url(client, path, name)
            
            if success:
                self.passed_pages.append({
                    'path': path,
                    'name': name,
                    'status': status_code,
                    'message': message
                })
                self.stdout.write(
                    f"{Fore.GREEN}[PASS]{Style.RESET_ALL} | "
                    f"{path:50} | {name:30} | {Fore.GREEN}{status_code}{Style.RESET_ALL}"
                )
            else:
                self.failed_pages.append({
                    'path': path,
                    'name': name,
                    'status': status_code,
                    'message': message
                })
                self.stdout.write(
                    f"{Fore.RED}[FAIL]{Style.RESET_ALL} | "
                    f"{path:50} | {name:30} | {Fore.RED}{status_code or 'ERROR'}{Style.RESET_ALL}"
                )
        
        # Write summary
        self._write_summary()
        
        # Write to log file
        self._write_log_file(log_file)
        
        # Exit with appropriate code
        if self.failed_pages:
            exit(1)
        else:
            exit(0)

    def _write_summary(self):
        """Write summary to terminal"""
        self.stdout.write(f"\n{Back.MAGENTA}{Fore.WHITE}{'='*80}{Style.RESET_ALL}")
        self.stdout.write(f"{Back.MAGENTA}{Fore.WHITE}  TEST SUMMARY{Style.RESET_ALL}")
        self.stdout.write(f"{Back.MAGENTA}{Fore.WHITE}{'='*80}{Style.RESET_ALL}\n")
        
        total = len(self.passed_pages) + len(self.failed_pages) + len(self.skipped_pages)
        
        self.stdout.write(
            f"{Fore.GREEN}[PASS] Passed: {len(self.passed_pages)}{Style.RESET_ALL} | "
            f"{Fore.RED}[FAIL] Failed: {len(self.failed_pages)}{Style.RESET_ALL} | "
            f"{Fore.YELLOW}[SKIP] Skipped: {len(self.skipped_pages)}{Style.RESET_ALL} | "
            f"{Fore.CYAN}Total: {total}{Style.RESET_ALL}\n"
        )
        
        if self.failed_pages:
            self.stdout.write(f"{Back.RED}{Fore.WHITE}FAILED PAGES:{Style.RESET_ALL}\n")
            for page in self.failed_pages:
                self.stdout.write(
                    f"  {Fore.RED}*{Style.RESET_ALL} {page['path']:50} "
                    f"({page['name']}) - {Fore.RED}{page['message']}{Style.RESET_ALL}"
                )
            self.stdout.write("")
        
        self.stdout.write(
            f"{Fore.CYAN}Log file saved to: {os.path.abspath('logs.txt')}{Style.RESET_ALL}\n"
        )

    def _write_log_file(self, log_file):
        """Write results to log file"""
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"PAGE LOADING TEST REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*80}\n\n")
            
            # Summary
            total = len(self.passed_pages) + len(self.failed_pages) + len(self.skipped_pages)
            f.write(f"SUMMARY\n")
            f.write(f"{'='*80}\n")
            f.write(f"[PASS] Passed:  {len(self.passed_pages)}\n")
            f.write(f"[FAIL] Failed:  {len(self.failed_pages)}\n")
            f.write(f"[SKIP] Skipped: {len(self.skipped_pages)}\n")
            f.write(f"Total: {total}\n\n")
            
            # Failed pages
            if self.failed_pages:
                f.write(f"FAILED PAGES\n")
                f.write(f"{'='*80}\n")
                for page in self.failed_pages:
                    f.write(f"\nPath:    {page['path']}\n")
                    f.write(f"Name:    {page['name']}\n")
                    f.write(f"Status:  {page['status'] or 'ERROR'}\n")
                    f.write(f"Message: {page['message']}\n")
                f.write(f"\n{'='*80}\n\n")
            
            # Passed pages
            f.write(f"PASSED PAGES ({len(self.passed_pages)})\n")
            f.write(f"{'='*80}\n")
            for page in self.passed_pages:
                f.write(f"{page['path']:50} ({page['name']:30}) - {page['status']}\n")
