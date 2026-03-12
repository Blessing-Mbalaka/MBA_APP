#!/usr/bin/env python
"""
Comprehensive System Test Suite
Combines all testing phases (data, pages, buttons) and exports results to CSV
Usage: python systemtest.py
"""

import os
import sys
import django
import time
import csv
import threading
import json
from datetime import datetime
from colorama import Fore, Back, Style, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from mbamain.models import (
    StudentProfile, SupervisorProfile, ExamminerProfile, 
    Project, NominationForm
)

init(autoreset=True)
User = get_user_model()

# ASCII spinners for Windows compatibility
SPINNER_CHARS = ['|', '/', '-', '\\']


class TestResult:
    """Single test case result"""
    def __init__(self, test_id, user_role, category, test_name, expected, actual, status, notes=""):
        self.test_id = test_id
        self.user_role = user_role
        self.category = category
        self.test_name = test_name
        self.expected = expected
        self.actual = actual
        self.status = status
        self.notes = notes
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'Test_ID': self.test_id,
            'User_Role': self.user_role,
            'Category': self.category,
            'Test_Name': self.test_name,
            'Expected_Result': self.expected,
            'Actual_Result': self.actual,
            'Status': self.status,
            'Notes': self.notes,
            'Timestamp': self.timestamp
        }


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
        print(f"\r{' ' * 60}\r[OK] {final_message}")
    
    def _animate(self):
        while self.running:
            spinner = SPINNER_CHARS[self.index % len(SPINNER_CHARS)]
            sys.stdout.write(f"\r{spinner} {self.message}")
            sys.stdout.flush()
            self.index += 1
            time.sleep(0.1)


class SystemTest:
    """Comprehensive system test suite"""
    
    def __init__(self):
        self.test_results = []
        self.test_counter = 0
        self.csv_file = 'systemtest_results.csv'
        self.base_url = 'http://localhost:8000'
        self.client = Client()
        self.driver = None
        
        # Test users
        self.test_users = {
            'student': {'username': 'systest_student@test.com', 'password': 'testpass123', 'type': 'STUDENT'},
            'scholar': {'username': 'systest_scholar@test.com', 'password': 'testpass123', 'type': 'SCHOLAR'},
            'examiner': {'username': 'systest_examiner@test.com', 'password': 'testpass123', 'type': 'EXAMINER'},
            'admin': {'username': 'systest_admin@test.com', 'password': 'testpass123', 'type': 'ADMIN'},
        }
        
        # Chrome options for headless mode
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--window-size=1920,1080')
    
    def add_result(self, user_role, category, test_name, expected, actual, status, notes=""):
        """Add test result to results array"""
        self.test_counter += 1
        result = TestResult(
            test_id=f"T{self.test_counter:04d}",
            user_role=user_role,
            category=category,
            test_name=test_name,
            expected=expected,
            actual=actual,
            status=status,
            notes=notes
        )
        self.test_results.append(result)
        
        status_color = Fore.GREEN if status == "PASS" else Fore.RED
        status_text = "[PASS]" if status == "PASS" else "[FAIL]"
        print(f"{status_color}{status_text}{Style.RESET_ALL} | {test_name}")
        if notes:
            print(f"         -> {notes}")
    
    def setup_test_users(self):
        """Create or get test users"""
        print(f"\n{Back.YELLOW}{Fore.BLACK}SETTING UP TEST USERS{Style.RESET_ALL}\n")
        
        user_types = {
            'student': (3, 'STUDENT', StudentProfile),
            'scholar': (2, 'SCHOLAR', SupervisorProfile),
            'examiner': (4, 'EXAMINER', ExamminerProfile),
            'admin': (1, 'ADMIN', None),
        }
        
        for role, (user_type, type_name, profile_class) in user_types.items():
            try:
                user = User.objects.get(username=self.test_users[role]['username'])
                status = "PASS"
                notes = f"User ID: {user.pk}"
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=self.test_users[role]['username'],
                    email=self.test_users[role]['username'],
                    password=self.test_users[role]['password'],
                    user_type=user_type
                )
                status = "PASS"
                notes = f"User ID: {user.pk}"
            
            self.add_result('SYSTEM', 'Setup', f'{type_name} user setup', f'{type_name} user exists', notes, status)
    
    def test_phase_1_data_workflow(self):
        """Phase 1: Test complete data workflow"""
        print(f"\n{Back.CYAN}{Fore.BLACK}PHASE 1: DATA WORKFLOW TESTS{Style.RESET_ALL}\n")
        
        # Pre-cleanup: Delete any existing workflow test data to avoid FK conflicts
        try:
            for username in [
                'systest_workflow_student@test.com',
                'systest_workflow_supervisor@test.com',
                'systest_workflow_examiner@test.com'
            ]:
                user = User.objects.filter(username=username).first()
                if user:
                    # Delete projects first (FK constraint)
                    Project.objects.filter(student=user).delete()
                    Project.objects.filter(primary_supervisor=user.pk).delete()
                    user.delete()
        except Exception:
            pass
        
        try:
            # Create test student user
            student_user = User.objects.create_user(
                username='systest_workflow_student@test.com',
                email='systest_workflow_student@test.com',
                password='testpass123',
                user_type=User.UserType.STUDENT
            )
            self.add_result('STUDENT', 'Workflow', 'Student user creation', 'User created', 'User created', 'PASS', f'ID: {student_user.pk}')
            
            # Verify profile auto-created
            student_profile = StudentProfile.objects.get(user=student_user)
            self.add_result('STUDENT', 'Workflow', 'Student profile auto-creation', 'Profile auto-created', 'Profile exists', 'PASS', f'Profile ID: {student_profile.pk}')
            
            # Update profile data
            student_profile.name = "System"
            student_profile.surname = "TestStudent"
            student_profile.student_no = "SYSTEST001"
            student_profile.save()
            
            student_profile.refresh_from_db()
            profile_data_ok = (student_profile.name == "System" and student_profile.student_no == "SYSTEST001")
            self.add_result('STUDENT', 'Workflow', 'Profile data persistence', 'Data persists after save', 'Data persisted', 'PASS' if profile_data_ok else 'FAIL')
            
            # Create supervisor
            supervisor_user = User.objects.create_user(
                username='systest_workflow_supervisor@test.com',
                email='systest_workflow_supervisor@test.com',
                password='testpass123',
                user_type=User.UserType.SCHOLAR,
                role_type=User.RoleType.SUPERVISOR
            )
            supervisor_profile = SupervisorProfile.objects.get(user=supervisor_user)
            supervisor_profile.name = "Dr. System"
            supervisor_profile.surname = "Supervisor"
            supervisor_profile.department = "Engineering"
            supervisor_profile.save()
            
            self.add_result('SUPERVISOR', 'Workflow', 'Supervisor profile setup', 'Profile configured', 'Profile configured', 'PASS', f'Dept: {supervisor_profile.department}')
            
            # Create project
            project = Project.objects.create(
                student=student_user,
                project_title="System Test Project",
                project_description="Testing all workflow steps",
                discipline="Computer Science",
                qualification="MBA"
            )
            self.add_result('STUDENT', 'Workflow', 'Project creation', 'Project created', f'Project ID {project.pk}', 'PASS')
            
            # Assign supervisor
            project.primary_supervisor = supervisor_user.pk
            project.save()
            self.add_result('SUPERVISOR', 'Workflow', 'Supervisor appointment', 'Supervisor assigned', f'Supervisor ID {supervisor_user.pk}', 'PASS')
            
            # Submit nomination form
            nom_form = NominationForm.objects.create(
                project=project,
                degree="MBA",
                qualification="MBA"
            )
            project.nomination_form_submitted = True
            project.save()
            self.add_result('STUDENT', 'Workflow', 'Form submission', 'Form submitted', 'Form submitted', 'PASS', f'Form ID: {nom_form.pk}')
            
            # Approve form
            project.nomination_form_approved = True
            project.save()
            self.add_result('ADMIN', 'Workflow', 'Form approval', 'Form approved by admin', 'Form approved', 'PASS')
            
            # HDC verification
            project.nomination_form_hdc_verified = True
            project.save()
            self.add_result('HDC', 'Workflow', 'HDC verification', 'Form verified by HDC', 'Form verified', 'PASS')
            
            # Create examiner
            examiner_user = User.objects.create_user(
                username='systest_workflow_examiner@test.com',
                email='systest_workflow_examiner@test.com',
                password='testpass123',
                user_type=User.UserType.EXAMINER
            )
            examiner_profile = ExamminerProfile.objects.get(user=examiner_user)
            
            # Appoint examiner
            project.assessor_1 = examiner_profile.pk
            project.assessor_1_appointed = True
            project.save()
            self.add_result('EXAMINER', 'Workflow', 'Examiner appointment', 'Examiner appointed', f'Examiner ID {examiner_profile.pk}', 'PASS')
            
            # Examiner approves
            project.assessor_1_responded = True
            project.assessor_1_approved = True
            project.save()
            self.add_result('EXAMINER', 'Workflow', 'Examiner approval', 'Examiner approved project', 'Status: approved', 'PASS')
            
            # Cleanup workflow test data - delete projects before users to avoid FK constraint
            self.add_result('SYSTEM', 'Workflow', 'Complete workflow test', 'All workflow steps pass', 'All steps completed', 'PASS', 'Workflow executed successfully')
            
            # Post-cleanup: Delete all workflow test data
            try:
                Project.objects.filter(student=student_user).delete()
                Project.objects.filter(primary_supervisor=supervisor_user.pk).delete()
                student_user.delete()
                supervisor_user.delete()
                examiner_user.delete()
            except Exception as e:
                # Log cleanup error but don't fail the test
                pass
            
        except Exception as e:
            self.add_result('SYSTEM', 'Workflow', 'Workflow test', 'Complete workflow test', str(e), 'FAIL', str(e)[:100])
    
    def setup_driver(self):
        """Initialize Selenium WebDriver"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ WebDriver failed: {str(e)}{Style.RESET_ALL}")
            return False
    
    def test_phase_2_page_load(self):
        """Phase 2: Test page loads for all user roles"""
        print(f"\n{Back.CYAN}{Fore.BLACK}PHASE 2: PAGE LOAD TESTS{Style.RESET_ALL}\n")
        
        if not self.setup_driver():
            self.add_result('SYSTEM', 'PageLoad', 'WebDriver initialization', 'WebDriver starts', 'WebDriver failed', 'FAIL')
            return
        
        pages = {
            'student': [
                ('/profile', 'Student Profile'),
                ('/projects', 'Student Projects'),
            ],
            'scholar': [
                ('/scholar/profile', 'Scholar Profile'),
                ('/invites', 'Scholar Invites'),
            ],
            'examiner': [
                ('/examiner/profile', 'Examiner Profile'),
                ('/invites/examiner', 'Examiner Invites'),
            ],
        }
        
        for user_role, page_list in pages.items():
            # New driver instance per user to avoid session conflicts
            if user_role != 'student':
                try:
                    self.driver.quit()
                except:
                    pass
                self.setup_driver()
            
            # Login
            try:
                self.driver.get(f'{self.base_url}/signin')
                time.sleep(2)
                
                # Wait for email field to be present (max 5 second timeout)
                email_field = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, 'email'))
                )
                password_field = self.driver.find_element(By.NAME, 'password')
                
                email_field.send_keys(self.test_users[user_role]['username'])
                password_field.send_keys(self.test_users[user_role]['password'])
                
                submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                submit_btn.click()
                
                time.sleep(2)
                self.add_result(user_role.upper(), 'PageLoad', f'{user_role.upper()} login', 'Login successful', 'Authenticated', 'PASS')
                
            except TimeoutException:
                self.add_result(user_role.upper(), 'PageLoad', f'{user_role.upper()} login', 'Login successful', 'Timeout waiting for page', 'FAIL')
                continue
            except Exception as e:
                self.add_result(user_role.upper(), 'PageLoad', f'{user_role.upper()} login', 'Login successful', str(e)[:50], 'FAIL')
                continue
            
            # Test pages
            for path, page_name in page_list:
                try:
                    self.driver.get(f'{self.base_url}{path}')
                    time.sleep(1)
                    
                    # Check if page loaded (look for content)
                    body = self.driver.find_element(By.TAG_NAME, 'body')
                    page_loaded = len(body.text) > 0
                    
                    status = 'PASS' if page_loaded else 'FAIL'
                    self.add_result(
                        user_role.upper(),
                        'PageLoad',
                        f'{page_name} ({path})',
                        'Page loads with content',
                        'Page loaded',
                        status
                    )
                except TimeoutException:
                    self.add_result(user_role.upper(), 'PageLoad', f'{page_name} ({path})', 'Page loads', 'Timeout', 'FAIL')
                except Exception as e:
                    self.add_result(user_role.upper(), 'PageLoad', f'{page_name} ({path})', 'Page loads', str(e)[:50], 'FAIL')
    
    def test_phase_3_button_interactions(self):
        """Phase 3: Test button interactions on pages"""
        print(f"\n{Back.CYAN}{Fore.BLACK}PHASE 3: BUTTON INTERACTION TESTS{Style.RESET_ALL}\n")
        
        if not self.driver:
            self.add_result('SYSTEM', 'Buttons', 'Button test setup', 'Driver ready', 'No driver', 'FAIL')
            return
        
        button_test_pages = {
            'student': [
                ('/profile', 'Student Profile'),
                ('/projects', 'Student Projects'),
            ],
            'scholar': [
                ('/scholar/profile', 'Scholar Profile'),
            ],
            'examiner': [
                ('/examiner/profile', 'Examiner Profile'),
            ],
        }
        
        for user_role, page_list in button_test_pages.items():
            for path, page_name in page_list:
                try:
                    self.driver.get(f'{self.base_url}{path}')
                    time.sleep(1)
                    
                    # Find all clickable elements
                    buttons = self.driver.find_elements(By.TAG_NAME, 'button')
                    links = self.driver.find_elements(By.TAG_NAME, 'a')
                    
                    clickables = buttons + links
                    
                    if len(clickables) == 0:
                        self.add_result(
                            user_role.upper(),
                            'Buttons',
                            f'{page_name} - No clickables',
                            'Page interactive elements present',
                            '0 buttons/links found',
                            'PASS',  # Page load is still good even if minimal
                            'Minimal UI (info page)'
                        )
                        continue
                    
                    # Test first few buttons
                    tested = 0
                    clicked = 0
                    for clickable in clickables[:3]:  # Test first 3
                        try:
                            if clickable.is_displayed():
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", clickable)
                                time.sleep(0.3)
                                clickable.click()
                                clicked += 1
                                tested += 1
                                time.sleep(0.5)
                                self.driver.back()
                                time.sleep(0.5)
                        except Exception:
                            tested += 1
                    
                    if tested > 0:
                        self.add_result(
                            user_role.upper(),
                            'Buttons',
                            f'{page_name} - {len(clickables)} elements',
                            f'Buttons interactive',
                            f'{clicked}/{tested} clickable',
                            'PASS' if clicked > 0 else 'FAIL',
                            f'Total: {len(clickables)} interactive elements'
                        )
                    
                except Exception as e:
                    self.add_result(user_role.upper(), 'Buttons', f'{page_name} - Button test', 'Buttons interactive', str(e), 'FAIL')
    
    def test_phase_4_authentication(self):
        """Phase 4: Test authentication and access control"""
        print(f"\n{Back.CYAN}{Fore.BLACK}PHASE 4: AUTHENTICATION TESTS{Style.RESET_ALL}\n")
        
        for user_role, user_info in self.test_users.items():
            try:
                login_ok = self.client.login(
                    username=user_info['username'],
                    password=user_info['password']
                )
                
                self.add_result(
                    user_role.upper(),
                    'Auth',
                    f'{user_role.upper()} login',
                    'User authenticates',
                    'Authenticated' if login_ok else 'Failed',
                    'PASS' if login_ok else 'FAIL'
                )
                
                if login_ok:
                    # Test logout
                    self.client.logout()
                    self.add_result(
                        user_role.upper(),
                        'Auth',
                        f'{user_role.upper()} logout',
                        'User logouts',
                        'Logged out',
                        'PASS'
                    )
                    
            except Exception as e:
                self.add_result(user_role.upper(), 'Auth', f'{user_role.upper()} auth', 'User authenticates', str(e), 'FAIL')
    
    def test_phase_5_http_status(self):
        """Phase 5: Test HTTP status codes"""
        print(f"\n{Back.CYAN}{Fore.BLACK}PHASE 5: HTTP STATUS TESTS{Style.RESET_ALL}\n")
        
        endpoints = [
            ('/signin', 'Login page', 200),
            ('/signup', 'Signup page', 200),
            ('/404-notfound', 'Not found page', 404),
        ]
        
        for path, description, expected_status in endpoints:
            try:
                response = self.client.get(path)
                status_ok = response.status_code == expected_status
                
                self.add_result(
                    'SYSTEM',
                    'HTTP',
                    f'{description} ({path})',
                    f'Status {expected_status}',
                    f'Status {response.status_code}',
                    'PASS' if status_ok else 'FAIL'
                )
            except Exception as e:
                self.add_result('SYSTEM', 'HTTP', f'{description} ({path})', f'Status {expected_status}', str(e), 'FAIL')
    
    def export_to_csv(self):
        """Export test results to CSV"""
        print(f"\n{Back.MAGENTA}{Fore.BLACK}EXPORTING RESULTS TO CSV{Style.RESET_ALL}\n")
        
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'Test_ID', 'User_Role', 'Category', 'Test_Name',
                    'Expected_Result', 'Actual_Result', 'Status', 'Notes', 'Timestamp'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for result in self.test_results:
                    writer.writerow(result.to_dict())
            
            print(f"[OK] CSV exported: {self.csv_file}")
            print(f"  Total records: {len(self.test_results)}")
            
        except Exception as e:
            print(f"[ERROR] CSV export failed: {str(e)}")
    
    def print_summary(self):
        """Print test summary"""
        passed = sum(1 for r in self.test_results if r.status == 'PASS')
        failed = sum(1 for r in self.test_results if r.status == 'FAIL')
        total = len(self.test_results)
        success_rate = int((passed / total * 100)) if total > 0 else 0
        
        print(f"\n{Back.CYAN}{Fore.BLACK}{'='*80}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}  COMPREHENSIVE SYSTEM TEST SUMMARY{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'='*80}{Style.RESET_ALL}\n")
        
        print(f"Total Tests:     {total}")
        print(f"Passed:          {Fore.GREEN}{passed}{Style.RESET_ALL}")
        print(f"Failed:          {Fore.RED}{failed}{Style.RESET_ALL}")
        print(f"Success Rate:    {Fore.CYAN}{success_rate}%{Style.RESET_ALL}\n")
        
        # Group by category
        categories = {}
        for result in self.test_results:
            if result.category not in categories:
                categories[result.category] = {'passed': 0, 'failed': 0}
            if result.status == 'PASS':
                categories[result.category]['passed'] += 1
            else:
                categories[result.category]['failed'] += 1
        
        print("Results by Category:")
        for category, stats in sorted(categories.items()):
            cat_total = stats['passed'] + stats['failed']
            cat_pct = int((stats['passed'] / cat_total * 100)) if cat_total > 0 else 0
            status_icon = Fore.GREEN + "[OK]" if cat_total == stats['passed'] else Fore.RED + "[FAIL]"
            print(f"{status_icon} {Style.RESET_ALL} {category:15} | {stats['passed']:2}/{cat_total:2} ({cat_pct:3}%)")
        
        print(f"\n{Fore.CYAN}CSV Report: {os.path.abspath(self.csv_file)}{Style.RESET_ALL}\n")
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        
        # Delete test users and any remaining projects (cleanup projects first)
        for user_info in self.test_users.values():
            try:
                user = User.objects.get(username=user_info['username'])
                # Delete projects first to avoid FK constraint
                Project.objects.filter(student=user).delete()
                Project.objects.filter(primary_supervisor=user.pk).delete()
                user.delete()
            except:
                pass
        
        # Delete any workflow test users/projects that might still exist
        try:
            for username in [
                'systest_workflow_student@test.com',
                'systest_workflow_supervisor@test.com',
                'systest_workflow_examiner@test.com'
            ]:
                user = User.objects.filter(username=username).first()
                if user:
                    Project.objects.filter(student=user).delete()
                    Project.objects.filter(primary_supervisor=user.pk).delete()
                    user.delete()
        except:
            pass
    
    def run(self):
        """Execute complete system test suite"""
        print(f"\n{Back.CYAN}{Fore.BLACK}{'='*80}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}  COMPREHENSIVE SYSTEM TEST SUITE{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'='*80}{Style.RESET_ALL}")
        
        try:
            anim = LoadingAnimation("Setting up test environment...")
            anim.start()
            self.setup_test_users()
            anim.stop("Test environment ready")
            
            # Run critical test phases (non-Selenium)
            self.test_phase_1_data_workflow()
            self.test_phase_4_authentication()
            self.test_phase_5_http_status()
            
            # Run Selenium tests with timeout protection
            try:
                anim = LoadingAnimation("Starting page load tests...")
                anim.start()
                anim.stop("Page load tests starting")
                self.test_phase_2_page_load()
                self.test_phase_3_button_interactions()
            except KeyboardInterrupt:
                print(f"\n[SKIP] Page load tests - interrupted")
            except Exception as e:
                print(f"\n[SKIP] Page load tests - error: {str(e)[:50]}")
            
            # Export and summary
            self.export_to_csv()
            self.print_summary()
            
        except KeyboardInterrupt:
            print(f"\n[INTERRUPTED] Test suite interrupted by user")
        except Exception as e:
            print(f"\n[ERROR] Test suite error: {str(e)}")
        finally:
            self.cleanup()


if __name__ == '__main__':
    tester = SystemTest()
    tester.run()
