#!/usr/bin/env python
"""
Robust Email System Test Script
Tests password reset token generation and email sending with pretty output
Run: python test_email_system.py
"""

import os
import sys
import django
from pprint import pprint
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from mbamain.models import AUser, PasswordResetToken
from mbamain.utils.shortcuts import send_reset_token
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_success(msg):
    """Print success message"""
    print(f"✅ {msg}")

def print_error(msg):
    """Print error message"""
    print(f"❌ {msg}")

def print_info(msg):
    """Print info message"""
    print(f"ℹ️  {msg}")

def print_section(title):
    """Print section header"""
    print(f"\n📋 {title}")
    print("-" * 70)

def test_user_exists():
    """Test if test user exists"""
    print_section("Test 1: Check Test User")
    try:
        user = AUser.objects.filter(email="student_1@test.mba.local").first()
        if user:
            print_success(f"Test user found: {user.email}")
            print(f"   Username: {user.username}")
            print(f"   User Type: {user.user_type}")
            return user
        else:
            print_error("Test user 'student_1@test.mba.local' not found")
            return None
    except Exception as e:
        print_error(f"Error checking user: {str(e)}")
        return None

def test_token_generation(user):
    """Test password reset token generation"""
    print_section("Test 2: Generate Password Reset Token")
    try:
        # Delete existing tokens for this user
        PasswordResetToken.objects.filter(user=user).delete()
        
        # Create new token
        token = PasswordResetToken.objects.create(
            user=user,
            token=PasswordResetToken.generate_token(),
            created_date=timezone.now(),
            max_time=60
        )
        
        print_success("Reset token generated successfully")
        print(f"   Token: {token.token}")
        print(f"   User: {token.user.email}")
        print(f"   Created: {token.created_date}")
        print(f"   Expires in: {token.max_time} minutes")
        print(f"   Expiration Time: {token.get_expiration_time()}")
        return token
    except Exception as e:
        print_error(f"Error generating token: {str(e)}")
        return None

def test_send_reset_email(user, token):
    """Test sending password reset email"""
    print_section("Test 3: Send Password Reset Email")
    try:
        print_info(f"Sending email to: {user.email}")
        print_info(f"Token: {token.token}")
        print("\n📨 Email Output Below:")
        print("-" * 70)
        
        # Send email (will print to console with console backend)
        send_reset_token(user.email, token.token)
        
        print("-" * 70)
        print_success("Email sent successfully!")
        return True
    except Exception as e:
        print_error(f"Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_token_validation(user, token):
    """Test token validation"""
    print_section("Test 4: Validate Reset Token")
    try:
        # Check if token exists
        existing_token = PasswordResetToken.objects.filter(
            token=token.token,
            user=user
        ).first()
        
        if existing_token:
            print_success("Token found in database")
            print(f"   Is Expired: {existing_token.has_expired()}")
            print(f"   Token Valid: {not existing_token.has_expired()}")
            return True
        else:
            print_error("Token not found in database")
            return False
    except Exception as e:
        print_error(f"Error validating token: {str(e)}")
        return False

def test_email_backend_config():
    """Test email backend configuration"""
    print_section("Test 5: Email Backend Configuration")
    try:
        from django.conf import settings
        
        backend = settings.EMAIL_BACKEND
        use_console = getattr(settings, 'USE_CONSOLE_EMAIL', False)
        
        print_info(f"Email Backend: {backend}")
        print_info(f"Using Console Backend: {use_console}")
        
        if "console" in backend.lower():
            print_success("✨ Console email backend is ACTIVE - emails will print to terminal")
        else:
            print_info("⚠️  SMTP backend configured - emails will be sent via SMTP")
        
        return True
    except Exception as e:
        print_error(f"Error checking configuration: {str(e)}")
        return False

def test_smtp_credentials():
    """Test SMTP credentials and connection"""
    print_section("Test 6: SMTP Configuration & Credentials")
    try:
        from django.conf import settings
        
        backend = settings.EMAIL_BACKEND
        
        # Skip if console backend
        if "console" in backend.lower():
            print_info("Console backend active - skipping SMTP tests")
            return True
        
        # Check SMTP configuration
        smtp_host = getattr(settings, 'EMAIL_HOST', None)
        smtp_port = getattr(settings, 'EMAIL_PORT', None)
        smtp_user = getattr(settings, 'EMAIL_HOST_USER', None)
        smtp_password = getattr(settings, 'EMAIL_HOST_PASSWORD', None)
        use_tls = getattr(settings, 'EMAIL_USE_TLS', None)
        use_ssl = getattr(settings, 'EMAIL_USE_SSL', None)
        
        print_info(f"SMTP Host: {smtp_host}")
        print_info(f"SMTP Port: {smtp_port}")
        print_info(f"SMTP User: {smtp_user}")
        print_info(f"Use TLS: {use_tls}")
        print_info(f"Use SSL: {use_ssl}")
        
        # Validate required fields
        if not all([smtp_host, smtp_port, smtp_user, smtp_password]):
            print_error("Missing SMTP credentials")
            return False
        
        print_success("All SMTP credentials configured")
        return True
    except Exception as e:
        print_error(f"Error checking SMTP configuration: {str(e)}")
        return False

def test_smtp_connection():
    """Test actual SMTP connection"""
    print_section("Test 7: SMTP Connection Test")
    try:
        from django.conf import settings
        import smtplib
        
        backend = settings.EMAIL_BACKEND
        
        # Skip if console backend
        if "console" in backend.lower():
            print_info("Console backend active - skipping SMTP connection test")
            return True
        
        smtp_host = getattr(settings, 'EMAIL_HOST', None)
        smtp_port = getattr(settings, 'EMAIL_PORT', None)
        smtp_user = getattr(settings, 'EMAIL_HOST_USER', None)
        smtp_password = getattr(settings, 'EMAIL_HOST_PASSWORD', None)
        use_tls = getattr(settings, 'EMAIL_USE_TLS', True)
        use_ssl = getattr(settings, 'EMAIL_USE_SSL', False)
        
        print_info(f"Connecting to {smtp_host}:{smtp_port}...")
        
        # Attempt connection
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        
        print_success("✨ SMTP connection successful")
        
        # Try TLS if configured
        if use_tls and not use_ssl:
            print_info("Starting TLS...")
            server.starttls()
            print_success("TLS started successfully")
        
        # Try login
        print_info(f"Authenticating as: {smtp_user}")
        server.login(smtp_user, smtp_password)
        print_success("✨ SMTP authentication successful")
        
        server.quit()
        print_success("✨ SMTP connection closed gracefully")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print_error(f"SMTP Authentication failed: {str(e)}")
        return False
    except smtplib.SMTPException as e:
        print_error(f"SMTP Error: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
        return False

def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All tests passed! Email system is working correctly.")
    else:
        print_error(f"{total - passed} test(s) failed. Check configuration.")

def main():
    """Run all tests"""
    print_header("🔐 ROBUST EMAIL SYSTEM TEST")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {}
    
    # Test 1: Check user exists
    user = test_user_exists()
    results["User Exists"] = user is not None
    
    if not user:
        print_error("Cannot continue tests without test user")
        print_summary(results)
        return
    
    # Test 2: Generate token
    token = test_token_generation(user)
    results["Token Generation"] = token is not None
    
    if not token:
        print_error("Cannot continue tests without token")
        print_summary(results)
        return
    
    # Test 3: Send email
    results["Send Email"] = test_send_reset_email(user, token)
    
    # Test 4: Validate token
    results["Token Validation"] = test_token_validation(user, token)
    
    # Test 5: Email backend config
    results["Email Backend Config"] = test_email_backend_config()
    
    # Test 6: SMTP credentials
    results["SMTP Credentials"] = test_smtp_credentials()
    
    # Test 7: SMTP connection
    results["SMTP Connection"] = test_smtp_connection()
    
    # Print summary
    print_summary(results)

if __name__ == "__main__":
    main()
