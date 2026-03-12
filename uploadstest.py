import os
import sys
import django

# Set up Django first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from mbamain.models import Cv, StudentProfile, SupervisorProfile, ExamminerProfile

User = get_user_model()

class CVUploadDownloadTest(TestCase):
    
    def setUp(self):
        """Create test user and authenticate"""
        self.client = Client()
        # Clean up any existing test user
        User.objects.filter(username='testexaminer@test.com').delete()
        
        self.user = User.objects.create_user(
            username='testexaminer@test.com',
            email='testexaminer@test.com',
            password='testpass123',
            user_type=4  # EXAMINER
        )
        # Profile should be auto-created by signals, but get_or_create just in case
        ExamminerProfile.objects.get_or_create(user=self.user)
        
    def test_cv_upload(self):
        """Test uploading a CV file"""
        print("\n=== Testing CV Upload ===")
        self.client.login(username='testexaminer@test.com', password='testpass123')
        
        # Create a fake PDF file
        pdf_content = b'%PDF-1.4\n%fake pdf content'
        test_file = SimpleUploadedFile(
            "test_cv.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        # Upload CV
        response = self.client.post('/upload/cv', {'cv': test_file}, follow=True)
        print(f"Upload response status: {response.status_code}")
        print(f"Upload response: {response}")
        
        # Check if CV was created in database
        cv = Cv.objects.filter(user=self.user).first()
        if cv:
            print(f"✓ CV created in database: {cv}")
            print(f"✓ CV file path: {cv.cv_file.name}")
            # Refresh user from DB to get updated has_cv
            self.user.refresh_from_db()
            print(f"✓ CV has_cv flag: {self.user.has_cv}")
            return True
        else:
            print("✗ CV not found in database")
            return False
    
    def test_cv_download(self):
        """Test downloading a CV file"""
        print("\n=== Testing CV Download ===")
        self.client.login(username='testexaminer@test.com', password='testpass123')
        
        # First create a CV
        pdf_content = b'%PDF-1.4\n%fake pdf content'
        test_file = SimpleUploadedFile(
            "test_cv.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        cv = Cv.objects.create(
            user=self.user,
            cv_file=test_file
        )
        self.user.has_cv = True
        self.user.save()
        
        print(f"Created CV: {cv}")
        print(f"CV file path: {cv.cv_file.path}")
        
        # Test download
        response = self.client.get(f'/download/cv?id={cv.id}')
        print(f"Download response status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✓ Download successful")
            print(f"✓ Content type: {response.get('Content-Type')}")
            print(f"✓ Content disposition: {response.get('Content-Disposition')}")
            return True
        else:
            print(f"✗ Download failed with status {response.status_code}")
            if response.status_code == 404:
                print(f"✗ Error: File not found - check file path")
            return False
    
    def test_cv_file_exists(self):
        """Test that uploaded CV file actually exists on disk"""
        print("\n=== Testing CV File Existence ===")
        self.client.login(username='testexaminer@test.com', password='testpass123')
        
        pdf_content = b'%PDF-1.4\n%fake pdf content'
        test_file = SimpleUploadedFile(
            "test_cv.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        cv = Cv.objects.create(
            user=self.user,
            cv_file=test_file
        )
        
        try:
            file_path = cv.cv_file.path
            print(f"File path: {file_path}")
            
            if os.path.exists(file_path):
                print(f"✓ File exists on disk")
                with open(file_path, 'rb') as f:
                    content = f.read()
                    print(f"✓ File content length: {len(content)} bytes")
                return True
            else:
                print(f"✗ File does not exist on disk")
                return False
        except Exception as e:
            print(f"✗ Error accessing file: {str(e)}")
            return False

if __name__ == '__main__':
    print("Starting CV Upload/Download Tests...\n")
    
    test = CVUploadDownloadTest()
    test.setUp()
    
    # Run tests using the same CV from upload test
    results = []
    upload_success = test.test_cv_upload()
    results.append(("Upload Test", upload_success))
    
    if upload_success:
        # If upload succeeded, test file and download with existing CV
        cv = Cv.objects.filter(user=test.user).first()
        if cv:
            print(f"\n=== Testing CV File Existence ===")
            try:
                file_path = cv.cv_file.path
                print(f"File path: {file_path}")
                
                if os.path.exists(file_path):
                    print(f"✓ File exists on disk")
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        print(f"✓ File content length: {len(content)} bytes")
                    results.append(("File Exists Test", True))
                else:
                    print(f"✗ File does not exist on disk")
                    results.append(("File Exists Test", False))
            except Exception as e:
                print(f"✗ Error accessing file: {str(e)}")
                results.append(("File Exists Test", False))
            
            # Now test download with this CV
            print(f"\n=== Testing CV Download ===")
            # Make sure client is authenticated
            test.client.login(username='testexaminer@test.com', password='testpass123')
            response = test.client.get(f'/download/cv?id={cv.id}')
            print(f"Download response status: {response.status_code}")
            if response.status_code == 302:
                print(f"Redirect location: {response.get('Location')}")
                # Follow redirect
                response = test.client.get(response['Location'])
                print(f"After redirect - status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✓ Download successful")
                print(f"✓ Content type: {response.get('Content-Type')}")
                print(f"✓ Content disposition: {response.get('Content-Disposition')}")
                results.append(("Download Test", True))
            else:
                print(f"✗ Download failed with status {response.status_code}")
                if response.status_code == 404:
                    print(f"✗ Error: File not found - check file path")
                results.append(("Download Test", False))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
