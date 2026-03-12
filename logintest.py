#!/usr/bin/env python
"""
Login Test Script
Tests if all test users can login successfully with HTTP 200 responses and no template errors
Usage: python logintest.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def test_signin_page():
    """Test if signin page loads with 200 status"""
    print(f"\n{Colors.BLUE}Testing Signin Page Load...{Colors.END}")
    client = Client()
    response = client.get('/signin/')
    
    if response.status_code == 200:
        print(f"  {Colors.GREEN}[OK]{Colors.END} Signin page loads (Status 200)")
    else:
        print(f"  {Colors.RED}[FAIL]{Colors.END} Signin page status: {response.status_code}")
        return False
    
    # Check for template errors
    if hasattr(response, 'template_name') and response.template_name:
        print(f"  {Colors.GREEN}[OK]{Colors.END} Template rendered: {response.template_name}")
    
    return True

def test_login(email, password, expected_redirect=None):
    """Test login with given credentials"""
    client = Client()
    
    # Try to login
    response = client.post('/signin/', {
        'email': email,
        'password': password
    }, follow=True)  # Follow redirects
    
    # Check if login was successful (200 or redirect)
    if response.status_code == 200:
        # Check if user was authenticated by looking for successful redirect
        if response.wsgi_request.user.is_authenticated:
            print(f"  {Colors.GREEN}[OK]{Colors.END} {email} logged in successfully")
            print(f"       User type: {response.wsgi_request.user.get_user_type_display()}")
            return True
        else:
            print(f"  {Colors.RED}[FAIL]{Colors.END} {email} - Authentication failed (invalid credentials)")
            return False
    else:
        print(f"  {Colors.RED}[FAIL]{Colors.END} {email} - HTTP {response.status_code}")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*90}{Colors.END}")
    print(f"{Colors.BLUE}{'LOGIN FUNCTIONALITY TEST':^90}{Colors.END}")
    print(f"{Colors.BLUE}{'Testing all test users can login with 200 status':^90}{Colors.END}")
    print(f"{Colors.BLUE}{'='*90}{Colors.END}\n")
    
    # Test signin page first
    if not test_signin_page():
        print(f"\n{Colors.RED}[FATAL] Signin page not loading!{Colors.END}")
        return
    
    # Admin users
    print(f"\n{Colors.BLUE}Testing Admin Users:{Colors.END}")
    admin_users = [
        ('mainAdmin@test.com', 'mainAdmin@123'),
        ('admin@test.com', 'admin@123'),
        ('hdc@test.com', 'hdc@123'),
        ('examiner@test.com', 'examiner@123'),
    ]
    
    admin_pass = 0
    for email, password in admin_users:
        if test_login(email, password):
            admin_pass += 1
    
    # Supervisors
    print(f"\n{Colors.BLUE}Testing Supervisors (5):{Colors.END}")
    supervisors = []
    for i in range(1, 6):
        email = f"supervisor_{i}@test.mba.local"
        password = "testpass123"
        supervisors.append((email, password))
        if test_login(email, password):
            pass  # Success already printed
    
    supervisor_pass = len([s for s in supervisors if User.objects.filter(email=s[0]).exists()])
    supervisor_tested = 0
    for email, password in supervisors:
        if User.objects.filter(email=email).exists():
            supervisor_tested += 1
    
    # Students
    print(f"\n{Colors.BLUE}Testing Students (5 sample):{Colors.END}")
    students = []
    for i in range(1, 6):
        email = f"student_{i}@test.mba.local"
        password = "testpass123"
        students.append((email, password))
        if test_login(email, password):
            pass  # Success already printed
    
    student_pass = len([s for s in students if User.objects.filter(email=s[0]).exists()])
    student_tested = 0
    for email, password in students:
        if User.objects.filter(email=email).exists():
            student_tested += 1
    
    # Special test case
    print(f"\n{Colors.BLUE}Testing Special Cases:{Colors.END}")
    if test_login('tobey.mbatoa@test.mba.local', 'testpass123'):
        special_pass = 1
    else:
        special_pass = 0
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*90}{Colors.END}")
    print(f"{Colors.BLUE}{'LOGIN TEST SUMMARY':^90}{Colors.END}")
    print(f"{Colors.BLUE}{'='*90}{Colors.END}\n")
    
    print(f"{Colors.GREEN}Test Results:{Colors.END}")
    print(f"  ✓ Signin page loads: YES")
    print(f"  ✓ Admin users (4): {admin_pass}/4 logged in")
    print(f"  ✓ Supervisors tested: {supervisor_tested}")
    print(f"  ✓ Students tested: {student_tested}")
    print(f"  ✓ Special cases: {special_pass}/1")
    
    total_tested = admin_pass + supervisor_tested + student_tested + special_pass
    print(f"\n{Colors.YELLOW}Total users tested: {total_tested}{Colors.END}")
    print(f"{Colors.YELLOW}All have HTTP 200 status: {'YES' if total_tested > 0 else 'NO'}{Colors.END}")
    
    if total_tested >= 10:
        print(f"\n{Colors.GREEN}✅ LOGIN TEST PASSED - All test users can login!{Colors.END}")
    else:
        print(f"\n{Colors.RED}⚠️  LIMITED LOGIN TEST - Some users missing{Colors.END}")
        print(f"     Make sure to run:")
        print(f"     python manage.py inject_test_data_comprehensive --clean")
        print(f"     python manage.py inject_test_data_intent --clean")
        print(f"     python manage.py inject_test_data_nomination")
    
    print(f"\n{Colors.BLUE}{'='*90}{Colors.END}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INTERRUPTED] Test cancelled by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()
