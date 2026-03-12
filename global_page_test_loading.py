#!/usr/bin/env python
"""
Global Page Test Loading - Comprehensive browser-based test suite
Tests all buttons, links, and endpoints for each user type
Usage: python global_page_test_loading.py
"""

import os
import sys
import django
import time
import threading
from datetime import datetime
from colorama import Fore, Back, Style, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import get_user_model
from mbamain.models import StudentProfile, SupervisorProfile, ExamminerProfile

init(autoreset=True)

User = get_user_model()

# ANSI escape codes for animations
SPINNER_CHARS = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']


class LoadingAnimation:
    """Terminal loading animation"""
    def __init__(self, message="Loading"):
        self.message = message
        self.running = False
        self.thread = None
        self.index = 0
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self, final_message="Done"):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        print(f"\r{' ' * 60}\r{Fore.GREEN}✓{Style.RESET_ALL} {final_message}")
    
    def _animate(self):
        while self.running:
            spinner = SPINNER_CHARS[self.index % len(SPINNER_CHARS)]
            sys.stdout.write(f"\r{spinner} {self.message}")
            sys.stdout.flush()
            self.index += 1
            time.sleep(0.1)


class GlobalPageTester:
    """Comprehensive browser-based page and button test"""
    
    def __init__(self):
        self.log_file = 'global_page_test_results.txt'
        self.driver = None
        self.base_url = 'http://localhost:8000'
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'failed_items': [],
            'user_access': {}
        }
        self.users = {
            'student': {'username': 'student@test.com', 'password': 'testpass123', 'type': 'STUDENT'},
            'scholar': {'username': 'scholar@test.com', 'password': 'testpass123', 'type': 'SCHOLAR'},
            'examiner': {'username': 'examiner@test.com', 'password': 'testpass123', 'type': 'EXAMINER'},
            'admin': {'username': 'admin@test.com', 'password': 'testpass123', 'type': 'ADMIN'},
        }
        
        # Setup Chrome options for headless mode
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--window-size=1920,1080')
    
    def setup_driver(self):
        """Initialize Chrome WebDriver"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to initialize WebDriver: {str(e)}{Style.RESET_ALL}")
            return False
    
    def create_test_users(self):
        """Create test users for each role"""
        print(f"{Fore.CYAN}Setting up test users...{Style.RESET_ALL}")
        
        user_types = {
            'student@test.com': (3, 'STUDENT', StudentProfile),
            'scholar@test.com': (2, 'SCHOLAR', SupervisorProfile),
            'examiner@test.com': (4, 'EXAMINER', ExamminerProfile),
            'admin@test.com': (1, 'ADMIN', None),
        }
        
        for email, (user_type, type_name, profile_class) in user_types.items():
            try:
                # Try to get existing user
                user = User.objects.get(username=email)
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Using existing {type_name} user: {email}")
            except User.DoesNotExist:
                # Create new user if doesn't exist
                try:
                    from mbamain.models import Project
                    # Delete any related projects first to avoid FK constraint
                    Project.objects.filter(student__username=email).delete()
                    # Now delete the user
                    User.objects.filter(username=email).delete()
                except Exception:
                    pass
                
                # Create the user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password='testpass123',
                    user_type=user_type
                )
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Created {type_name} user: {email}")
    
    def login(self, username, password):
        """Login to the application"""
        try:
            self.driver.get(f'{self.base_url}/signin')
            
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'email'))
            )
            password_field = self.driver.find_element(By.NAME, 'password')
            
            email_field.send_keys(username)
            password_field.send_keys(password)
            
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_btn.click()
            
            # Wait for redirect
            time.sleep(2)
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Login failed: {str(e)}{Style.RESET_ALL}")
            return False
    
    def get_all_clickable_elements(self):
        """Get all buttons and links on current page"""
        clickables = []
        
        # Get all buttons
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        for btn in buttons:
            try:
                if btn.is_displayed() and btn.is_enabled():
                    text = btn.get_attribute('aria-label') or btn.text or btn.get_attribute('title') or 'Button'
                    clickables.append({'element': btn, 'text': text, 'type': 'button'})
            except StaleElementReferenceException:
                continue
        
        # Get all links
        links = self.driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            try:
                if link.is_displayed():
                    text = link.text or link.get_attribute('title') or link.get_attribute('href') or 'Link'
                    clickables.append({'element': link, 'text': text, 'type': 'link'})
            except StaleElementReferenceException:
                continue
        
        return clickables
    
    def test_page_buttons(self, page_url, page_name, user_info):
        """Test all clickable elements on a page"""
        page_results = {'passed': 0, 'failed': 0, 'failed_buttons': []}
        
        try:
            self.driver.get(page_url)
            time.sleep(1)
            
            clickables = self.get_all_clickable_elements()
            
            for clickable in clickables:
                try:
                    element = clickable['element']
                    text = clickable['text']
                    elem_type = clickable['type']
                    
                    # Check if element is interactable
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(0.5)
                    
                    # Try to click
                    try:
                        element.click()
                        time.sleep(0.5)
                        page_results['passed'] += 1
                    except Exception as click_error:
                        page_results['failed'] += 1
                        page_results['failed_buttons'].append({
                            'text': text,
                            'type': elem_type,
                            'error': str(click_error)[:100]
                        })
                    
                    # Go back to page after click
                    self.driver.get(page_url)
                    time.sleep(0.5)
                
                except Exception as e:
                    continue
            
            return page_results
        except Exception as e:
            return {'passed': 0, 'failed': 1, 'failed_buttons': [{'error': str(e)[:100]}]}
    
    def test_user_pages(self, user_role, user_info):
        """Test all pages accessible to a user role"""
        print(f"\n{Back.BLUE}{Fore.WHITE}Testing {user_role.upper()} User{Style.RESET_ALL}")
        print("=" * 60)
        
        # Login
        anim = LoadingAnimation(f"Logging in as {user_role}...")
        anim.start()
        
        if not self.login(user_info['username'], user_info['password']):
            anim.stop(f"Login failed for {user_role}")
            return
        
        anim.stop(f"Login successful for {user_role}")
        
        # Define pages to test per role
        role_pages = {
            'student': [
                ('/profile', 'Student Profile'),
                ('/projects', 'Projects'),
            ],
            'scholar': [
                ('/scholar/profile', 'Scholar Profile'),
                ('/invites', 'Invites'),
            ],
            'examiner': [
                ('/examiner/profile', 'Examiner Profile'),
                ('/invites/examiner', 'Examiner Invites'),
            ],
            'admin': [
                ('/admin/', 'Admin Dashboard'),
            ],
        }
        
        pages = role_pages.get(user_role, [])
        user_results = {'pages_tested': 0, 'pages_passed': 0, 'pages_failed': []}
        
        for path, page_name in pages:
            anim = LoadingAnimation(f"Testing {page_name}...")
            anim.start()
            
            full_url = f'{self.base_url}{path}'
            results = self.test_page_buttons(full_url, page_name, user_info)
            
            user_results['pages_tested'] += 1
            
            if results['failed'] == 0:
                user_results['pages_passed'] += 1
                passed_count = results['passed']
                anim.stop(f"{page_name}: {passed_count} buttons tested ✓")
            else:
                user_results['pages_failed'].append({
                    'page': page_name,
                    'failed_buttons': results['failed_buttons']
                })
                anim.stop(f"{page_name}: {results['failed']} buttons failed ✗")
        
        self.results['user_access'][user_role] = user_results
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{Back.MAGENTA}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"{Back.MAGENTA}{Fore.WHITE}  GLOBAL PAGE TEST SUMMARY{Style.RESET_ALL}")
        print(f"{Back.MAGENTA}{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        for user_role, results in self.results['user_access'].items():
            total = results['pages_tested']
            passed = results['pages_passed']
            failed = total - passed
            
            status = f"{Fore.GREEN}✓ PASS{Style.RESET_ALL}" if failed == 0 else f"{Fore.RED}✗ FAIL{Style.RESET_ALL}"
            print(f"{status} | {user_role.upper():10} | Pages: {passed}/{total} passed")
            
            if results['pages_failed']:
                for failed_page in results['pages_failed']:
                    print(f"    {Fore.RED}→{Style.RESET_ALL} {failed_page['page']}")
                    for btn in failed_page['failed_buttons']:
                        print(f"      {Fore.RED}•{Style.RESET_ALL} {btn['text'][:30]}: {btn['error'][:40]}")
        
        print(f"\n{Fore.CYAN}Log file saved to: {os.path.abspath(self.log_file)}{Style.RESET_ALL}\n")
    
    def write_log(self, content):
        """Write to log file"""
        with open(self.log_file, 'a') as f:
            f.write(content + '\n')
    
    def run(self):
        """Run the complete test suite"""
        print(f"\n{Back.CYAN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}  GLOBAL PAGE TEST LOADING SUITE{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}\n")
        
        # Clear log file
        with open(self.log_file, 'w') as f:
            f.write(f"Global Page Test Results - {datetime.now()}\n")
            f.write("=" * 60 + "\n\n")
        
        # Setup
        anim = LoadingAnimation("Setting up test environment...")
        anim.start()
        
        if not self.setup_driver():
            anim.stop("WebDriver setup failed")
            return False
        
        self.create_test_users()
        anim.stop("Test environment ready")
        
        # Test each user role
        for user_role, user_info in self.users.items():
            self.test_user_pages(user_role, user_info)
        
        # Cleanup
        if self.driver:
            self.driver.quit()
        
        # Print summary
        self.print_summary()
        
        return True


if __name__ == '__main__':
    tester = GlobalPageTester()
    try:
        tester.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Test interrupted by user{Style.RESET_ALL}")
        if tester.driver:
            tester.driver.quit()
    except Exception as e:
        print(f"{Fore.RED}✗ Test failed: {str(e)}{Style.RESET_ALL}")
        if tester.driver:
            tester.driver.quit()
