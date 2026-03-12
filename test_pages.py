#!/usr/bin/env python
"""
Standalone page loading test script for MBA Application
Usage: python test_pages.py
"""

import os
import sys
import django
from django.test import Client
from django.urls import get_resolver, URLPattern, URLResolver
from colorama import Fore, Back, Style, init
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Initialize colorama
init(autoreset=True)


class PageLoadingTester:
    def __init__(self, log_file='logs.txt'):
        self.log_file = log_file
        self.failed_pages = []
        self.passed_pages = []
        self.client = Client()

    def get_all_urls(self, urlpatterns, prefix=''):
        """Recursively extract all URL patterns"""
        urls = []
        for pattern in urlpatterns:
            if isinstance(pattern, URLResolver):
                new_prefix = prefix + str(pattern.pattern)
                urls.extend(self.get_all_urls(pattern.url_patterns, new_prefix))
            elif isinstance(pattern, URLPattern):
                full_pattern = prefix + str(pattern.pattern)
                urls.append({
                    'pattern': full_pattern,
                    'name': pattern.name,
                })
        return urls

    def extract_url_path(self, pattern):
        """Convert URL pattern to testable path"""
        import re
        path = str(pattern)
        
        if '<' in path:
            path = path.replace('<int:', '<')
            path = path.replace('<str:', '<')
            path = path.replace('>', '')
            path = re.sub(r'<.*?>', '1', path)
        
        path = '/' + path if not path.startswith('/') else path
        return path

    def test_url(self, path, url_name):
        """Test a single URL"""
        try:
            response = self.client.get(path, follow=True)
            
            if response.status_code == 404:
                return False, response.status_code, "Page not found (404)"
            elif response.status_code >= 500:
                return False, response.status_code, f"Server error ({response.status_code})"
            elif response.status_code in [200, 301, 302]:
                return True, response.status_code, "OK"
            else:
                return False, response.status_code, f"Unexpected status ({response.status_code})"
        except Exception as e:
            return False, None, str(e)

    def run(self):
        """Run the test suite"""
        self.print_header()
        
        resolver = get_resolver()
        all_urls = self.get_all_urls(resolver.url_patterns)
        
        print(f"{Fore.YELLOW}Found {len(all_urls)} URL patterns{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Testing URLs...{Style.RESET_ALL}\n")
        
        for url_info in all_urls:
            pattern = url_info['pattern']
            name = url_info['name'] or 'unnamed'
            path = self.extract_url_path(pattern)
            
            success, status_code, message = self.test_url(path, name)
            
            if success:
                self.passed_pages.append({
                    'path': path,
                    'name': name,
                    'status': status_code,
                    'message': message
                })
                print(
                    f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} | "
                    f"{path:50} | {name:30} | {Fore.GREEN}{status_code}{Style.RESET_ALL}"
                )
            else:
                self.failed_pages.append({
                    'path': path,
                    'name': name,
                    'status': status_code,
                    'message': message
                })
                print(
                    f"{Fore.RED}✗ FAIL{Style.RESET_ALL} | "
                    f"{path:50} | {name:30} | {Fore.RED}{status_code or 'ERROR'}{Style.RESET_ALL}"
                )
        
        self.print_summary()
        self.write_log_file()
        
        return len(self.failed_pages) == 0

    def print_header(self):
        """Print the test header"""
        print(f"\n{Back.CYAN}{Fore.BLACK}{'='*80}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}  PAGE LOADING TEST SUITE{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'='*80}{Style.RESET_ALL}\n")

    def print_summary(self):
        """Print the test summary"""
        print(f"\n{Back.MAGENTA}{Fore.WHITE}{'='*80}{Style.RESET_ALL}")
        print(f"{Back.MAGENTA}{Fore.WHITE}  TEST SUMMARY{Style.RESET_ALL}")
        print(f"{Back.MAGENTA}{Fore.WHITE}{'='*80}{Style.RESET_ALL}\n")
        
        total = len(self.passed_pages) + len(self.failed_pages)
        
        print(
            f"{Fore.GREEN}✓ Passed: {len(self.passed_pages)}{Style.RESET_ALL} | "
            f"{Fore.RED}✗ Failed: {len(self.failed_pages)}{Style.RESET_ALL} | "
            f"{Fore.CYAN}Total: {total}{Style.RESET_ALL}\n"
        )
        
        if self.failed_pages:
            print(f"{Back.RED}{Fore.WHITE}FAILED PAGES:{Style.RESET_ALL}\n")
            for page in self.failed_pages:
                print(
                    f"  {Fore.RED}•{Style.RESET_ALL} {page['path']:50} "
                    f"({page['name']}) - {Fore.RED}{page['message']}{Style.RESET_ALL}"
                )
            print()
        
        print(
            f"{Fore.CYAN}Log file saved to: {os.path.abspath(self.log_file)}{Style.RESET_ALL}\n"
        )

    def write_log_file(self):
        """Write results to log file"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"PAGE LOADING TEST REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*80}\n\n")
            
            # Summary
            total = len(self.passed_pages) + len(self.failed_pages)
            f.write(f"SUMMARY\n")
            f.write(f"{'='*80}\n")
            f.write(f"Passed:  {len(self.passed_pages)}\n")
            f.write(f"Failed:  {len(self.failed_pages)}\n")
            f.write(f"Total:   {total}\n\n")
            
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
            f.write(f"PASSED PAGES\n")
            f.write(f"{'='*80}\n")
            f.write(f"Total: {len(self.passed_pages)}\n\n")
            for page in self.passed_pages:
                f.write(f"{page['path']:50} ({page['name']:30}) - {page['status']}\n")


if __name__ == '__main__':
    tester = PageLoadingTester()
    success = tester.run()
    sys.exit(0 if success else 1)
